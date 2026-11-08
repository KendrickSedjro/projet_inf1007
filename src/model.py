import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from abc import abstractmethod

class Model:
    def __init__(self, dataframe: pd.DataFrame):
        self.X = dataframe[['OVR','SHO','DRI','DEF','PHY','Acceleration','Sprint Speed','Positioning','Shot Power','Long Shots','Volleys','Penalties','Vision','Crossing']]
        self.y = dataframe[['Finishing','PAC','PAS','Ball Control']]

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.model = None
        self.model_path = Path(__file__).resolve().parent.parent / 'model' / 'mon_model.joblib'

    def split_data_set(self) -> None:
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, random_state=42, test_size=0.4)
        
    @abstractmethod
    def train(self) -> None:
        pass

    def predire_feature(self, y_test = None) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("Le modèle n'est pas encore implémenté.")
        if self.X_test is None:
            raise ValueError("Les données de test ne sont pas encore initialisées.")
        if y_test is None:
            y_test = self.y_test

        y_pred = pd.DataFrame(
            self.model.predict(self.X_test),
            columns=self.y.columns,
            index=self.X_test.index,
        )
        if y_test is not None:
            self.metrics(y_true=y_test, y_pred=y_pred)
        return y_pred

    def features_importance(self) -> None:
        if self.model == None:
            raise ValueError("Le modèle n'est pas encore implémenté.")
        features = pd.DataFrame(self.model.feature_importances_, index=self.X.columns)
        print(features)

    def metrics(self, y_true: pd.DataFrame, y_pred: pd.DataFrame) -> pd.DataFrame:
        baseline = pd.DataFrame(
            {column: self.y_train[column].mean() for column in self.y.columns},
            index=y_true.index,
        )
        results = pd.DataFrame(
            {
                "MAE modèle": {
                    column: mean_absolute_error(y_true[column], y_pred[column])
                    for column in self.y.columns
                },
                "RMSE modèle": {
                    column: np.sqrt(mean_squared_error(y_true[column], y_pred[column]))
                    for column in self.y.columns
                },
                "R² modèle": {
                    column: r2_score(y_true[column], y_pred[column])
                    for column in self.y.columns
                },
                "MAE référence": {
                    column: mean_absolute_error(y_true[column], baseline[column])
                    for column in self.y.columns
                },
                "RMSE référence": {
                    column: np.sqrt(mean_squared_error(y_true[column], baseline[column]))
                    for column in self.y.columns
                },
                "R² référence": {
                    column: r2_score(y_true[column], baseline[column])
                    for column in self.y.columns
                },
            }
        )
        results.loc["Moyenne des cibles"] = results.mean()
        print("Évaluation sur les données de test (modèle comparé à la référence moyenne) :")
        print(results.to_string(float_format=lambda value: f"{value:.3f}"))
        return results

    def tracer_predictions_vs_reel(
        self,
        y_true: pd.DataFrame,
        y_pred: pd.DataFrame,
        chemin: Path | None = None,
    ) -> Path:
        """Trace et enregistre un nuage de points prédit/réel pour chaque cible."""
        if not y_true.columns.equals(y_pred.columns):
            raise ValueError("Les colonnes des valeurs réelles et prédites doivent correspondre.")
        if chemin is None:
            chemin = Path(__file__).resolve().parent.parent / "model" / "predictions_vs_reel.png"
        chemin.parent.mkdir(parents=True, exist_ok=True)

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        for ax, target in zip(axes.flat, y_true.columns):
            actual = y_true[target]
            predicted = y_pred[target]
            minimum = min(actual.min(), predicted.min())
            maximum = max(actual.max(), predicted.max())
            ax.scatter(actual, predicted, alpha=0.25, s=12)
            ax.plot([minimum, maximum], [minimum, maximum], "r--", label="Prédiction parfaite")
            ax.set(
                title=target,
                xlabel="Valeur réelle",
                ylabel="Valeur prédite",
                xlim=(minimum, maximum),
                ylim=(minimum, maximum),
            )
            ax.set_aspect("equal", adjustable="box")
            ax.legend()

        fig.suptitle("Valeurs prédites vs réelles")
        fig.tight_layout()
        fig.savefig(chemin, dpi=150)
        plt.close(fig)
        return chemin

    def save_model(self) -> None:
        joblib.dump(self.model, self.model_path, compress=3)






class RF_model(Model): 
    """
        Le random forest c'est modèle qui a plusieurs arbres et chaque arbres
        va s'entrainer sur une partie du dataset pigé aléatoirement avec remise

        Pour chaque arbre il aura des noeuds (c'est le moment ou l'arbre choisi des
        colonnes aléatoire pour évaluer les données) et il va poser une question exemple : 
        feature > 0.2 ce qui va le permettre de sépare le dataset en deux (V/F) et a la fin
        avec les séparation faite au fil des noeuds il va voir celle qui englobe le plus de 
        données et poser des seuils d'importance pour chaque features
        
        Le model va par la suite faire une  moyenne a partir des seuil enregistrées 
        par les arbres ce qui va le permettre de trouver un seuil d'importance moyen

        c'est utile notamment pour empecher l'overtffitting, car en séparant le dataset ca
        empeche le modele de surapprendre sur une seule colonne qui pourrais biaisé le model 
    """

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe=dataframe)  
        self.train()

    def choisir_hyperparams(self) :
        """
            Fonction qui entraine un modele en fonction de différents
            hyperparameters pour améliorer l'accuracy (fait avec l'IA)  
        """

        param_grid = {
            'n_estimators': [50, 100, 200],        # Nombre d'arbres
            'max_depth': [None, 10, 20],           # Profondeur maximale/ nombre d'étage de l'arbre
            'min_samples_split': [2, 5, 10],       # Échantillons min pour couper un nœud
            'max_features': ['sqrt', 'log2']       # Nombre de caractéristiques par nœud
        }

        grid_search = GridSearchCV(
            estimator=RandomForestRegressor(random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='neg_mean_absolute_error',
            n_jobs=-1            # Utiliser tous les processeurs de la machine pour aller plus vite
        )

        # 5. Lancer la recherche sur les données
        grid_search.fit(self.X_train, self.y_train)

        # 6. Afficher les meilleurs résultats
        print("Meilleurs hyperparamètres trouvés :")
        print(grid_search.best_params_)

        print("\nMeilleure MAE moyenne en validation croisée :", -grid_search.best_score_)
        return grid_search

    def train(self) -> None:
        self.split_data_set()
        grid_search = self.choisir_hyperparams()
        self.model = grid_search.best_estimator_ # choisi le meilleur modele
        self.model.fit(self.X_train, self.y_train)

"""
Code pour configurer le model....

df = pd.read_csv(Path(__file__).resolve().parent.parent / 'donnees' / 'raw' / 'all_players.csv')
mon_modele = RF_model(df)
y_pred = mon_modele.predire_feature()
mon_modele.save_model()
graphique = mon_modele.tracer_predictions_vs_reel(mon_modele.y_test, y_pred)
print("Graphique enregistré :", graphique)
"""
df = pd.read_csv(
    Path(__file__).resolve().parent.parent
    / "donnees" / "raw" / "all_players.csv"
)

modele = joblib.load(
    Path(__file__).resolve().parent.parent
    / "model" / "mon_model.joblib"
)

X = df[modele.feature_names_in_]
predictions = pd.DataFrame(
    modele.predict(X),
    columns=["Finishing", "PAC", "PAS", "Ball Control"],
    index=df.index,
)

print(predictions.head())