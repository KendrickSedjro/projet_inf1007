from abc import ABC, abstractmethod
import json
from pathlib import Path

import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor

from metriques import rmse, r2
from donnees import ENCODAGES_CATEGORIELS, charger_donnees


STATS = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
FEATURES = [
    "Acceleration",
    "Sprint Speed",
    "Positioning",
    "Shot Power",
    "Long Shots",
    "Volleys",
    "Penalties",
    "Vision",
    "Crossing",
    "Preferred foot" 
]

class Model(ABC):
    def __init__(self, dataframe: pd.DataFrame):
        self.X = dataframe[FEATURES]
        self.y = dataframe[STATS]

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.model = None
        self.model_path = Path(__file__).resolve().parent.parent / 'model' / 'mon_model.joblib'
        self.metadata_path = self.model_path.with_suffix(".json")

    def split_data_set(self) -> None:
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, random_state=42, test_size=0.4
        )

    @abstractmethod
    def entrainer(self) -> None:
        pass

    def importance_colonnes(self) -> None:
        " Fonction qui affiche l'importance de chaque colonnes dans la prédiction de la statistique"
        if self.model is None:
            raise ValueError("Le modèle n'est pas encore implémenté.")
        features = pd.DataFrame(self.model.feature_importances_, index=self.X.columns)
        print(features)

    def validation_modele(self, y_true: pd.DataFrame, y_pred: pd.DataFrame) -> pd.DataFrame:
        " Fonction qui affiche les métriques RMSE et r2 et les compare au baseline"

        if self.y_train is None:
            raise ValueError("Les données d'entraînement ne sont pas initialisées.")
        
        baseline = pd.DataFrame(
            {column: self.y_train[column].mean() for column in self.y.columns},
            index=y_true.index,
        )
        results = pd.DataFrame(
            {
                "RMSE modèle": {
                    column: rmse(y_true[column], y_pred[column])
                    for column in self.y.columns
                },

                "R² modèle": {
                    column: r2(y_true[column], y_pred[column])
                    for column in self.y.columns
                },
                "RMSE référence": {
                    column: rmse(y_true[column], baseline[column])
                    for column in self.y.columns
                },
                "R² référence": {
                    column: r2(y_true[column], baseline[column])
                    for column in self.y.columns
                },
            }
        )

        results.loc["Moyenne des cibles"] = results.mean()
        print("Évaluation sur les données de test (modèle comparé à la référence moyenne) :\n")
        print(results.to_string(float_format=lambda value: f"{value:.3f}"))
        return results

    def sauvegarder_modele(self) -> None:
        " Fonction qui enregistre le modele dans un format joblib"
        if self.model is None:
            raise ValueError("Le modèle n'est pas encore entraîné.")
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path, compress=3)

    def sauvegarder_metadonnees(self, resultats_test: pd.DataFrame) -> None:
        if self.model is None:
            raise ValueError("Le modèle n'est pas encore entraîné.")
        if self.X_test is None or self.y_test is None:
            raise ValueError("Les données de test ne sont pas initialisées.")

        variables = {}
        for colonne in self.X.columns:
            valeurs = self.X[colonne]
            if pd.api.types.is_numeric_dtype(valeurs):
                variables[colonne] = {
                    "type": "numerique",
                    "minimum": float(valeurs.min()),
                    "maximum": float(valeurs.max()),
                }
            else:
                variables[colonne] = {
                    "type": "categorielle",
                    "valeurs": sorted(valeurs.dropna().astype(str).unique().tolist()),
                }

        metadonnees = {
            "input_columns": list(self.X.columns),
            "target_columns": list(self.y.columns),
            "variables": variables,
            "categorical_encodings": ENCODAGES_CATEGORIELS,
            "metrics": {
                "rmse_test": {
                    colonne: float(resultats_test.loc[colonne, "RMSE modèle"])
                    for colonne in self.y.columns
                },
                "r2_test": {
                    colonne: float(resultats_test.loc[colonne, "R² modèle"])
                    for colonne in self.y.columns
                },
            },
        }
        with self.metadata_path.open("w", encoding="utf-8") as fichier:
            json.dump(metadonnees, fichier, ensure_ascii=False, indent=2)

    def tracer_predictions_vs_reel(self) -> Path:
        " Fonction qui trace les prédictions et en x valeur réelle et en y valeur prédite  "
        if self.model is None:
            raise ValueError("Le modèle n'est pas encore entraîné.")
        if self.X_test is None or self.y_test is None:
            raise ValueError("Les données de test ne sont pas initialisées.")

        predictions = pd.DataFrame(
            self.model.predict(self.X_test),
            columns=self.y.columns,
            index=self.y_test.index,
        )

        figure, axes = plt.subplots(2, 3, figsize=(18, 12))
        figure.suptitle("Valeurs prédites vs réelles", fontsize=18)

        for stat, ax in zip(self.y.columns, axes.flat):
            ax.scatter(
                self.y_test[stat],
                predictions[stat],
                alpha=0.3,
                s=14,
                label="Joueurs",
            )
            ax.plot(
                [0, 100],
                [0, 100],
                color="red",
                linestyle="--",
                linewidth=2,
                label="Prédiction parfaite",
            )
            ax.set(
                title=stat,
                xlabel="Valeur réelle",
                ylabel="Valeur prédite",
                xlim=(0, 100),
                ylim=(0, 100),
            )
            ax.legend(frameon=False, loc="upper left")

        figure.tight_layout(rect=(0, 0, 1, 0.96), pad=2)
        chemin_graphique = self.model_path.parent / "predictions_vs_reel.png"
        chemin_graphique.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(chemin_graphique, dpi=150, bbox_inches="tight")
        plt.close(figure)
        return chemin_graphique


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
        self.entrainer()

    def choisir_hyperparams(self):
        """
            Fonction qui entraine un modele en fonction de différents
            hyperparameters pour réduire l'écart de prédiction (fait avec l'IA)  

            retourne l'objet grid_search qui contient l'ensemble des modèles et param testé
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
            scoring="neg_mean_absolute_error",
            n_jobs=-1,
        )

        grid_search.fit(self.X_train, self.y_train)

        print("Meilleurs hyperparamètres trouvés :")
        print(grid_search.best_params_)

        return grid_search

    def entrainer(self) -> None:
        " Fonction qui entraine le model"
        self.split_data_set()
        grid_search = self.choisir_hyperparams()
        self.model = grid_search.best_estimator_
        self.model.fit(self.X_train, self.y_train)


def configurer_modele() -> RF_model:
    " Fonction qui configure le modèle"
    df = charger_donnees()
    class_model = RF_model(df)
    y_pred = pd.DataFrame(
        class_model.model.predict(class_model.X_test),
        columns=class_model.y.columns,
        index=class_model.X_test.index,
    )
    resultats_test = class_model.validation_modele(class_model.y_test, y_pred)
    class_model.importance_colonnes()
    class_model.sauvegarder_modele()
    class_model.sauvegarder_metadonnees(resultats_test)
    print(f"Graphique enregistré : {class_model.tracer_predictions_vs_reel()}")
    return class_model

if __name__ == "__main__":
    configurer_modele()
