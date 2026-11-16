"""Graphique d'exploration des données."""
import matplotlib.pyplot as plt
import pandas as pd

from donnees import charger_donnees, nettoyer_donnees

STATS = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]


def tracer_distributions(df: pd.DataFrame,
                         chemin: str = "donnees/exploration_stats.png") -> str:
    """Trace l'histogramme des 6 stats principales et l'enregistre.

    Reçoit un DataFrame nettoyé et le chemin de l'image.
    Renvoie le chemin du fichier créé.
    """
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    for ax, stat in zip(axes.flat, STATS):
        ax.hist(df[stat], bins=30)
        ax.set_title(stat)
        ax.set_xlabel("Note")
        ax.set_ylabel("Nombre de joueurs")
    fig.suptitle("Distribution des 6 stats principales (hors gardiens)")
    fig.tight_layout()
    fig.savefig(chemin)
    plt.close(fig)
    return chemin


if __name__ == "__main__":
    donnees = nettoyer_donnees(charger_donnees())
    print("Graphique enregistré :", tracer_distributions(donnees))