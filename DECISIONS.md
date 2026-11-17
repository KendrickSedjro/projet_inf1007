# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Sport, immobilier | Sport (football) : on connaît le domaine, ce qui permet de juger si les résultats ont du sens | à valider |
| Jeu de données | Kaggle EA FC 25 (stats de joueurs), NBA 2026 | EA FC 25 : 17 737 joueurs, licence Apache 2.0 vérifiée sur Kaggle. NBA écartée (trop peu de joueurs) | à valider |
| Cible | Note globale (OVR), valeur marchande, Ballon d'Or, poste, plusieurs stats | Les 6 stats principales (PAC, SHO, PAS, DRI, DEF, PHY), au choix de l'utilisateur. OVR écartée (calculée à partir des autres stats). Valeur marchande impossible (absente du CSV). Ballon d'Or écarté (trop peu de gagnants) | à valider |
| Entrées du modèle | Toutes les colonnes, sous-stats seulement, sous-stats + variables catégorielles | Sous-stats numériques (Acceleration, Sprint Speed, Positioning, Shot Power, Long Shots, Volleys, Penalties, Vision, Crossing) | à valider |
| Gardiens | Les garder, les retirer | Retirés : leurs colonnes (GK Diving, etc.) sont vides pour les autres joueurs | à valider |
| Métrique | RMSE, R² | RMSE (en points de stat) et R², comparés à la référence « prédire la moyenne » | à valider |
| Modèle | Régression linéaire, forêt aléatoire | Forêt aléatoire à plusieurs sorties (une pour chaque stat) | à valider |
| Technologie d'interface | Tkinter, Streamlit | Streamlit | à valider |