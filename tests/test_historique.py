"""Tests de src/historique.py (fichier temporaire de pytest)."""
from historique import ajouter_prediction, lire_historique


def test_historique_vide_si_fichier_absent(tmp_path):
    assert lire_historique(str(tmp_path / "absent.csv")) == []


def test_ajouter_puis_lire(tmp_path):
    chemin = str(tmp_path / "h.csv")
    ajouter_prediction("PAS", {"PAC": 80, "Age": 25}, 71.46, chemin)
    lignes = lire_historique(chemin)
    assert len(lignes) == 1
    assert lignes[0]["cible"] == "PAS"
    assert lignes[0]["prediction"] == "71.5"
    assert "PAC=80" in lignes[0]["entrees"]


def test_en_tete_ecrit_une_seule_fois(tmp_path):
    chemin = str(tmp_path / "h.csv")
    ajouter_prediction("PAS", {"PAC": 80}, 70.0, chemin)
    ajouter_prediction("SHO", {"PAC": 60}, 55.0, chemin)
    with open(chemin, encoding="utf-8") as f:
        assert f.read().count("date,cible") == 1
    assert len(lire_historique(chemin)) == 2


def test_cree_le_dossier_manquant(tmp_path):
    chemin = str(tmp_path / "sous" / "dossier" / "h.csv")
    ajouter_prediction("DEF", {"PHY": 70}, 60.0, chemin)
    assert len(lire_historique(chemin)) == 1