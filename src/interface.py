import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from pathlib import Path
from donnees import charger_donnees, nettoyer_donnees
from metriques import r2, rmse
STATS = ["Finishing", "PAC", "PAS", "Ball Control"]


st.set_page_config(
    page_title="FootPredictor",
    page_icon="⚽",
    layout="wide",
)


def tracer_predictions_vs_reel(
        y_true: pd.Series,
        y_pred: pd.Series,
        stat: str
    ):

    def droite_regression():
        fig1, ax = plt.subplots(figsize=(8, 5))
        ax.set_axisbelow(True)
        ax.grid(linewidth=0.8)
        ax.scatter(
            y_true,
            y_pred,
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
            title=f"Valeurs réelles et prédites — {stat}",
            xlabel="Valeur réelle",
            ylabel="Valeur prédite",
            xlim=(0, 100),
            ylim=(0, 100),
        )
        ax.legend(frameon=False, loc="upper left")
        fig1.tight_layout(pad=2)
        return fig1

    def histogramme():
        fig2, ax = plt.subplots(figsize=(8, 5))
        ax.set_axisbelow(True)
        ax.grid(axis="y", linewidth=0.8)
        ax.hist(
            [y_true, y_pred],
            bins=20,
            range=(0, 100),
            alpha=0.65,
            label=["Réel", "Prédit"],
        )
        ax.set(
            title=f"Distribution — {stat}",
            xlabel="Valeur",
            ylabel="Nombre de joueurs",
        )
        ax.legend(frameon=False)
        fig2.tight_layout(pad=2)
        return fig2

    return droite_regression(), histogramme()

def interface_principale():
    st.title("⚽ FootPredictor")
    st.caption("Comparez les valeurs réelles et prédites d’une statistique de joueur.")
    st.divider()

    with st.form("formulaire_prediction"):
        col_stat, col_bouton = st.columns([3, 1])
        with col_stat:
            stat = st.selectbox("Statistique à analyser", STATS)
        with col_bouton:
            st.write("")
            lancer_prediction = st.form_submit_button(
                "Lancer l’analyse",
                type="primary",
                use_container_width=True,
            )

    if lancer_prediction:
        donnees = nettoyer_donnees(charger_donnees())
        model = joblib.load(
            Path(__file__).resolve().parent.parent / "model" / "mon_model.joblib"
        )
        X = donnees[model.feature_names_in_]

        predictions = pd.DataFrame(
            model.predict(X),
            columns=STATS,
            index=donnees.index,
        )
        y_pred = predictions[stat]

        reg, hist = tracer_predictions_vs_reel(
            y_true=donnees[stat],
            y_pred=y_pred,
            stat=stat,
        )

        st.subheader(f"Résultats pour {stat}")
        col_graphique, col_histogramme = st.columns(2)

        with col_graphique:
            st.pyplot(reg, use_container_width=True)

        with col_histogramme:
            st.pyplot(hist, use_container_width=True)

        st.subheader("Qualité des prédictions")

        met_r2, met_rmse = st.columns(2)
        met_r2.metric(
            "Coefficient R²",
            f"{r2(donnees[stat], y_pred):.3f}",
            help="1 indique une prédiction parfaite; une valeur proche de 0 indique un résultat comparable à la moyenne.",
        )
        met_rmse.metric(
            "Erreur moyenne (RMSE)",
            f"{rmse(donnees[stat], y_pred):.2f} points",
            help="Écart moyen entre les valeurs réelles et prédites; plus cette valeur est faible, mieux c’est.",
        )

        plt.close(reg)
        plt.close(hist)


interface_principale()