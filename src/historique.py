import csv
import os
from datetime import datetime

CHEMIN_HISTORIQUE = os.path.join("donnees", "historique.csv")
COLONNES = ["date", "cible", "entrees", "prediction"]


def ajouter_prediction(cible: str, entrees: dict, prediction: float,
                       chemin: str = CHEMIN_HISTORIQUE) -> None:
    """Ajoute une prédiction à la fin du fichier (le crée avec l'en-tête au besoin).

    Reçoit la stat prédite, le dictionnaire des entrées et la valeur prédite.
    """
    existe = os.path.exists(chemin)
    dossier = os.path.dirname(chemin)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    with open(chemin, "a", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f)
        if not existe:
            ecrivain.writerow(COLONNES)
        ecrivain.writerow([
            datetime.now().isoformat(timespec="seconds"),
            cible,
            "; ".join(f"{k}={v}" for k, v in entrees.items()),
            f"{prediction:.1f}",
        ])


def lire_historique(chemin: str = CHEMIN_HISTORIQUE) -> list[dict]:
    """Renvoie la liste des prédictions (la plus récente en premier).

    Renvoie une liste vide si le fichier n'existe pas encore.
    """
    if not os.path.exists(chemin):
        return []
    with open(chemin, newline="", encoding="utf-8") as f:
        lignes = list(csv.DictReader(f))
    return sorted(lignes, key=lambda ligne: ligne["date"], reverse=True)