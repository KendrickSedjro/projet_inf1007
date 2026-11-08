"""Métriques d'évaluation calculées avec NumPy (sans boucle Python)."""
import numpy as np

from src.exceptions import DonneeInvalideError


def _preparer(y_vrai, y_pred) -> tuple[np.ndarray, np.ndarray]:
    """Convertit en tableaux NumPy et vérifie que les tailles concordent."""
    y_vrai = np.asarray(y_vrai, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_vrai.shape != y_pred.shape or y_vrai.size == 0:
        raise DonneeInvalideError("Les valeurs vraies et prédites doivent avoir la même taille (non vide).")
    return y_vrai, y_pred


def rmse(y_vrai, y_pred) -> float:
    """Erreur quadratique moyenne (en points de stat). Plus c'est petit, mieux c'est."""
    y_vrai, y_pred = _preparer(y_vrai, y_pred)
    return float(np.sqrt(np.mean((y_vrai - y_pred) ** 2)))


def r2(y_vrai, y_pred) -> float:
    """Coefficient de détermination R². 1 = parfait, 0 = pas mieux que la moyenne."""
    y_vrai, y_pred = _preparer(y_vrai, y_pred)
    ss_res = np.sum((y_vrai - y_pred) ** 2)
    ss_tot = np.sum((y_vrai - np.mean(y_vrai)) ** 2)
    if ss_tot == 0:
        raise DonneeInvalideError("R² indéfini : les valeurs vraies sont toutes identiques.")
    return float(1 - ss_res / ss_tot)