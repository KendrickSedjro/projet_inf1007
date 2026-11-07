"""Chargement et nettoyage du jeu de données EA FC 25."""
import os
import pandas as pd
import math
from abc import ABC, abstractmethod

from src.exceptions import DonneeInvalideError

CHEMIN_CSV = os.path.join("donnees", "raw", "all_players.csv")

COLONNES_A_RETIRER = [
    "Unnamed: 0", "Unnamed: 0.1", "Rank", "Name", "url",
    "play style", "Alternative positions",
]

def charger_donnees(chemin: str = CHEMIN_CSV) -> pd.DataFrame:
    """Lit le CSV et renvoie un DataFrame.

    Reçoit le chemin du fichier. Renvoie un DataFrame pandas.
    Échoue avec FileNotFoundError si le fichier n'existe pas.
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with open(chemin, encoding="utf-8") as f:
        return pd.read_csv(f)


def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    """Retire les gardiens et les colonnes inutiles, convertit taille et poids.

    Reçoit un DataFrame brut. Renvoie une copie nettoyée.
    """
    df = df[df["Position"] != "GK"].copy()
    colonnes_gk = [c for c in df.columns if c.startswith("GK")]
    a_retirer = [c for c in COLONNES_A_RETIRER + colonnes_gk if c in df.columns]
    df = df.drop(columns=a_retirer)
    for col in ("Height", "Weight"):
        df[col] = df[col].astype(str).str.extract(r"(\d+)", expand=False).astype(float)
    return df

class Variable(ABC):
    """Classe abstraite représentant une variable du jeu de données.

    Chaque sous-classe doit définir la méthode `valider` pour vérifier
    si une valeur est valide pour cette variable.
    """

    def __init__(self, nom: str) -> None:
        self._nom = nom

    @property
    def nom(self) -> str:
        """Nom de la colonne."""
        return self._nom

    @abstractmethod
    def valider(self, valeur) -> bool:
        """Vérifie si la valeur est valide pour cette variable.

        Doit être implémentée par les sous-classes.
        """
        pass

    def __repr__(self) -> str:
            return f"{type(self).__name__}({self._nom!r})"

class VariableNumerique(Variable):
    """Variable numérique avec un intervalle autorisé."""
    
    def __init__(self, nom: str, minimum: float, maximum: float) -> None:
            super().__init__(nom)
            self._minimum = float(minimum)
            self._maximum = float(maximum)

    def valider(self, valeur) -> float:
        texte = str(valeur).strip()
        if texte == "":
           raise DonneeInvalideError(f"{self._nom} : saisie vide.")
        try:
            nombre = float(texte.replace(",", "."))
        except ValueError:
            raise DonneeInvalideError(f"{self._nom} : '{texte}' n'est pas un nombre.") from None
        if not math.isfinite(nombre) or not (self._minimum <= nombre <= self._maximum):
            raise DonneeInvalideError(
                f"{self._nom} : entre {self._minimum:g} et {self._maximum:g} attendu."
            )
        return nombre

    def __str__(self) -> str:
        return f"{self._nom} (nombre entre {self._minimum:g} et {self._maximum:g})"

class VariableCategorielle(Variable):
    """Variable catégorique avec un ensemble de valeurs autorisées."""

    def __init__(self, nom: str, valeurs: list[str]) -> None:
            super().__init__(nom)
            self._valeurs = [str(v) for v in valeurs]

    @property
    def valeurs(self) -> list[str]:
            """Valeurs possibles (copie)."""
            return list(self._valeurs)

    def valider(self, valeur) -> str:
        texte = str(valeur).strip()
        if texte not in self._valeurs:
            raise DonneeInvalideError(f"{self._nom} : '{texte}' n'est pas un choix valide.")
        return texte

    def __str__(self) -> str:
        return f"{self._nom} (choix : {', '.join(self._valeurs)})"

def construire_variables(df: pd.DataFrame, colonnes_num: list[str], colonnes_cat: list[str]) -> list[Variable]:
    """Construit les variables d'entrée à partir des données.
     Les intervalles viennent des min et max des colonnes numériques,
    les choix viennent des valeurs distinctes des colonnes catégorielles.
    """
    variables: list[Variable] = [
         VariableNumerique(c, df[c].min(), df[c].max()) for c in colonnes_num
         ]
    variables += [VariableCategorielle(c, sorted(df[c].unique())) for c in colonnes_cat]
    return variables