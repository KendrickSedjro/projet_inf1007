import json
from types import SimpleNamespace

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.model import FEATURES, STATS, Model, RF_model


class ModeleTest(Model):
    def entrainer(self) -> None:
        pass


def creer_donnees(nombre: int = 12) -> pd.DataFrame:
    donnees = {
        feature: list(range(nombre))
        for feature in FEATURES
    }
    donnees.update(
        {
            stat: [valeur + index for valeur in range(nombre)]
            for index, stat in enumerate(STATS)
        }
    )
    return pd.DataFrame(donnees)


def test_validation_compare_le_modele_a_la_reference():
    modele = ModeleTest(creer_donnees())
    modele.y_train = modele.y.iloc[:8]
    y_true = modele.y.iloc[8:]

    resultats = modele.validation_modele(y_true, y_true.copy())

    assert (resultats["RMSE modèle"] == 0).all()
    assert (resultats["R² modèle"] == 1).all()
    assert (resultats["RMSE référence"] > 0).all()
    assert (resultats["R² référence"] < 1).all()


def test_foret_entraine_les_statistiques_utilisees_par_interface(monkeypatch):
    monkeypatch.setattr(
        RF_model,
        "choisir_hyperparams",
        lambda self: SimpleNamespace(
            best_estimator_=RandomForestRegressor(n_estimators=2, random_state=42)
        ),
    )

    modele = RF_model(creer_donnees())
    predictions = modele.model.predict(modele.X_test)

    assert list(modele.y.columns) == ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
    assert predictions.shape == (len(modele.X_test), len(STATS))


def test_sauvegarde_cree_le_dossier_parent(tmp_path):
    modele = ModeleTest(creer_donnees())
    modele.model = RandomForestRegressor(n_estimators=1, random_state=42).fit(
        modele.X, modele.y
    )
    modele.model_path = tmp_path / "nouveau" / "modele.joblib"

    modele.sauvegarder_modele()

    assert modele.model_path.is_file()


def test_sauvegarde_metadonnees_decrit_variables_et_metriques(tmp_path):
    modele = ModeleTest(creer_donnees())
    modele.split_data_set()
    modele.model = RandomForestRegressor(n_estimators=1, random_state=42).fit(
        modele.X_train, modele.y_train
    )
    predictions = pd.DataFrame(
        modele.model.predict(modele.X_test),
        columns=STATS,
        index=modele.y_test.index,
    )
    resultats = modele.validation_modele(modele.y_test, predictions)
    modele.metadata_path = tmp_path / "model.json"

    modele.sauvegarder_metadonnees(resultats)
    metadonnees = json.loads(modele.metadata_path.read_text(encoding="utf-8"))

    assert metadonnees["input_columns"] == FEATURES
    assert metadonnees["target_columns"] == STATS
    assert metadonnees["variables"]["Acceleration"] == {
        "type": "numerique",
        "minimum": 0.0,
        "maximum": 11.0,
    }
    assert set(metadonnees["metrics"]) == {"rmse_test", "r2_test"}


def test_tracer_predictions_vs_reel_cree_le_graphique(tmp_path):
    modele = ModeleTest(creer_donnees())
    modele.split_data_set()
    modele.model = RandomForestRegressor(n_estimators=1, random_state=42).fit(
        modele.X_train, modele.y_train
    )
    modele.model_path = tmp_path / "modele.joblib"

    chemin_graphique = modele.tracer_predictions_vs_reel()

    assert chemin_graphique == tmp_path / "predictions_vs_reel.png"
    assert chemin_graphique.is_file()