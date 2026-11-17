import json
from pathlib import Path

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from donnees import charger_donnees
from historique import ajouter_prediction


st.set_page_config(page_title="FootPredictor",page_icon="⚽",layout="wide",)

def tracer_predictions_vs_reel(y_true: pd.Series, y_pred: pd.Series,stat: str):

    def droite_regression():
        fig1, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(y_true,y_pred,alpha=0.3,s=14,label="Joueurs",)
        ax.plot([0, 100],[0, 100],color="red",linestyle="--",linewidth=2,
            label="Prédiction parfaite",)
        ax.set(title=f"Valeurs réelles et prédites — {stat}",xlabel="Valeur réelle",
            ylabel="Valeur prédite",xlim=(0, 100),ylim=(0, 100))

        ax.legend(frameon=False, loc="upper left")
        fig1.tight_layout(pad=2)
        return fig1

    def histogramme():
        fig2, ax = plt.subplots(figsize=(8, 5))
        ax.set_axisbelow(True)
        ax.grid(axis="y", linewidth=0.8)
        ax.hist([y_true, y_pred],bins=20,range=(0, 100),
            alpha=0.65,label=["Réel", "Prédit"])
        ax.set(title=f"Distribution — {stat}",xlabel="Valeur",
            ylabel="Nombre de joueurs",
        )
        ax.legend(frameon=False)
        fig2.tight_layout(pad=2)
        return fig2

    return droite_regression(), histogramme()

def interface_principale():
    
    dossier_modele = Path(__file__).resolve().parent.parent / "model"
    chemin_donnees = (
        Path(__file__).resolve().parent.parent
        / "donnees"
        / "processed"
        / "all_players.csv"
    )
    chemin_modele = dossier_modele / "mon_model.joblib"
    chemin_metadonnees = dossier_modele / "mon_model.json"
    
    with chemin_metadonnees.open(encoding="utf-8") as fichier:
        metadonnees = json.load(fichier)

    input_columns = metadonnees["input_columns"]
    target_columns = metadonnees["target_columns"]

    def en_tete():
        st.title("⚽ FootPredictor")
        st.caption("Comparez les valeurs réelles et prédites d’une statistique de joueur.")

    def predire_stat_joueur():
        donnees = charger_donnees(str(chemin_donnees))

        with st.form("formulaire_prediction_joueur"):
            nom_joueur = st.text_input(
                "Nom du joueur à rechercher",
                placeholder="Ex. Kylian Mbappé",
            )
            stat_a_predire = st.selectbox(
                "Statistique à prédire",target_columns
            )
            predire_joueur = st.form_submit_button(
                "Prédire la statistique du joueur",
                type="primary",
            )

        if not predire_joueur:
            return
        if not nom_joueur.strip():
            st.warning("Saisissez le nom d’un joueur avant de lancer sa prédiction.")
            return

        noms_joueurs = (
            donnees["Name"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.casefold()
        )
        indices_joueurs = noms_joueurs.index[
            noms_joueurs == nom_joueur.strip().casefold()
        ]
        if len(indices_joueurs) == 0:
            st.warning(
                f"Aucun joueur de champ trouvé sous le nom « {nom_joueur.strip()} »."
            )
            return

        model = joblib.load(chemin_modele)
        predictions_joueur = model.predict(
            donnees.loc[indices_joueurs, input_columns]
        )

        st.subheader(
            f"Prédiction de {stat_a_predire} pour {nom_joueur.strip()}"
        )
        index_stat = target_columns.index(stat_a_predire)
        for index, valeurs_predites in zip(indices_joueurs, predictions_joueur):
            joueur = donnees.loc[index]
            st.caption(
                f"{joueur['Name']} · Poste : {joueur['Position']} · "
                f"Équipe : {joueur['Team']}"
            )
            valeur_predite = valeurs_predites[index_stat]
            valeur_reelle = donnees.loc[index, stat_a_predire]
            col_predite, col_reelle = st.columns(2)
            col_predite.metric(
                f"{stat_a_predire} prédite",
                f"{valeur_predite:.1f}",
            )
            col_reelle.metric(
                f"{stat_a_predire} réelle",
                f"{valeur_reelle:.1f}",
            )

            entrees_joueur = donnees.loc[index, input_columns].to_dict()
            entrees_joueur.update(
                {
                    "Joueur": joueur["Name"],
                    "Poste": joueur["Position"],
                    "Équipe": joueur["Team"],
                }
            )

            ajouter_prediction(stat_a_predire, entrees_joueur, valeur_predite)
        st.success("La prédiction a été ajoutée à l’historique.")

    def statistiques_generales():
        donnees = charger_donnees(str(chemin_donnees))
        with st.form("formulaire_prediction_generale"):
            stat = st.selectbox("Statistique à analyser", target_columns)
            analyser = st.form_submit_button(
                "Analyser la statistique générale",
                type="primary",
            )

        if not analyser:
            return

        model = joblib.load(chemin_modele)
        predictions = pd.DataFrame(
            model.predict(donnees[input_columns]),
            columns=target_columns,
            index=donnees.index,
        )
        graphique, histogramme = tracer_predictions_vs_reel(
            y_true=donnees[stat],
            y_pred=predictions[stat],
            stat=stat,
        )

        st.subheader(f"Résultats pour {stat}")
        col_graphique, col_histogramme = st.columns(2)
        with col_graphique:
            st.pyplot(graphique, use_container_width=True)
        with col_histogramme:
            st.pyplot(histogramme, use_container_width=True)

        st.subheader("Qualité des prédictions")
        col_r2, col_rmse = st.columns(2)
        col_r2.metric(
            f"Coefficient R² — {stat}",
            f"{metadonnees['metrics']['r2_test'][stat]:.3f}",
            help="Score calculé sur les données de test lors de l'entraînement.",
        )
        col_rmse.metric(
            f"Erreur moyenne (RMSE) — {stat}",
            f"{metadonnees['metrics']['rmse_test'][stat]:.2f} points",
            help="Erreur calculée sur les données de test lors de l'entraînement; plus elle est faible, mieux c’est.",
        )
        plt.close(graphique)
        plt.close(histogramme)

    en_tete()
    onglet_joueur, onglet_general = st.tabs(
        ["Prédire les statistiques d’un joueur", "Statistiques générales des joueurs"]
    )
    with onglet_joueur:
        predire_stat_joueur()
    with onglet_general:
        statistiques_generales()

interface_principale()