"""Tests de la logique de src/donnees.py (sans l'interface)."""
import pandas as pd
import pytest

from donnees import (
    VariableCategorielle,
    VariableNumerique,
    charger_donnees,
    construire_variables,
    encoder_pied_preferre,
    nettoyer_donnees,
    preparer_donnees,
)
from exceptions import DonneeInvalideError


@pytest.fixture
def petit_df():
    return pd.DataFrame({
        "Position": ["ST", "GK", "CB"],
        "PAC": [80, 50, 60],
        "Height": ["180cm", "190cm", "185cm"],
        "Weight": ["75kg", "85kg", "80kg"],
        "GK Diving": [None, 80, None],
        "Name": ["a", "b", "c"],
        "Preferred foot": [" Right ", None, "left"],
    })


# --- VariableNumerique ---
def test_numerique_saisie_usuelle():
    assert VariableNumerique("PAC", 0, 100).valider("85") == pytest.approx(85.0)


def test_numerique_virgule_decimale():
    assert VariableNumerique("PAC", 0, 100).valider("85,5") == pytest.approx(85.5)


def test_numerique_bornes_acceptees():
    v = VariableNumerique("PAC", 0, 100)
    assert v.valider("0") == pytest.approx(0.0)
    assert v.valider("100") == pytest.approx(100.0)


def test_numerique_saisie_vide():
    with pytest.raises(DonneeInvalideError):
        VariableNumerique("PAC", 0, 100).valider("   ")


def test_numerique_non_numerique():
    with pytest.raises(DonneeInvalideError):
        VariableNumerique("PAC", 0, 100).valider("abc")


def test_numerique_hors_intervalle():
    with pytest.raises(DonneeInvalideError):
        VariableNumerique("PAC", 0, 100).valider("101")


def test_numerique_nan_refuse():
    with pytest.raises(DonneeInvalideError):
        VariableNumerique("PAC", 0, 100).valider("nan")


# --- VariableCategorielle ---
def test_categorielle_valide_et_espaces():
    v = VariableCategorielle("Position", ["ST", "CB"])
    assert v.valider(" ST ") == "ST"


def test_categorielle_invalide():
    with pytest.raises(DonneeInvalideError):
        VariableCategorielle("Position", ["ST", "CB"]).valider("XX")


def test_categorielle_valeurs_est_une_copie():
    v = VariableCategorielle("Position", ["ST", "CB"])
    v.valeurs.append("XX")
    assert v.valeurs == ["ST", "CB"]


# --- Données ---
def test_nettoyer_retire_gardiens_et_convertit(petit_df):
    df = nettoyer_donnees(petit_df)
    assert len(df) == 2
    assert "GK Diving" not in df.columns
    assert df["Name"].tolist() == ["a", "c"]
    assert df["Height"].tolist() == [180.0, 185.0]
    assert df["Preferred foot"].tolist() == [" Right ", "left"]


def test_encoder_pied_preferre_refuse_pied_inconnu():
    donnees = pd.DataFrame({"Preferred foot": ["Both"]})
    with pytest.raises(ValueError, match="Preferred foot"):
        encoder_pied_preferre(donnees)


def test_nettoyer_ne_encode_pas_le_pied_preferre(petit_df):
    donnees = nettoyer_donnees(petit_df)
    assert donnees["Preferred foot"].tolist() == [" Right ", "left"]


def test_encoder_pied_preferre_encode_texte_et_valeurs_deja_encodees():
    donnees = pd.DataFrame({"Preferred foot": [" Right ", "left", 1, 0]})

    encodees = encoder_pied_preferre(donnees)

    assert encodees["Preferred foot"].tolist() == [1, 0, 1, 0]
    assert donnees["Preferred foot"].tolist() == [" Right ", "left", 1, 0]


def test_encoder_pied_preferre_refuse_une_valeur_inconnue():
    donnees = pd.DataFrame({"Preferred foot": ["Both"]})

    with pytest.raises(ValueError, match="Preferred foot"):
        encoder_pied_preferre(donnees)


def test_preparer_donnees_enregistre_le_csv_traite(petit_df, tmp_path):
    chemin_source = tmp_path / "raw.csv"
    chemin_destination = tmp_path / "processed" / "all_players.csv"
    petit_df.to_csv(chemin_source, index=False)

    donnees = preparer_donnees(str(chemin_source), str(chemin_destination))

    assert chemin_destination.is_file()
    assert donnees["Name"].tolist() == ["a", "c"]
    assert charger_donnees(str(chemin_destination))["Preferred foot"].tolist() == [1, 0]


def test_charger_fichier_inexistant():
    with pytest.raises(FileNotFoundError):
        charger_donnees("donnees/raw/nexiste_pas.csv")


def test_construire_variables(petit_df):
    df = nettoyer_donnees(petit_df)
    vars_ = construire_variables(df, ["PAC"], ["Position"])
    assert isinstance(vars_[0], VariableNumerique)
    assert isinstance(vars_[1], VariableCategorielle)
    assert vars_[0].valider("60") == pytest.approx(60.0)
    with pytest.raises(DonneeInvalideError):
        vars_[0].valider("90")