# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Sport, immobilier | Sport (football) : on connaît le domaine, ce qui permet de juger si les résultats ont du sens | à valider |
| Jeu de données | Kaggle EA FC 25 (stats de joueurs), NBA 2026 | EA FC 25 : 17 737 joueurs, colonnes numériques et catégorielles (position, pied fort), assez de lignes. NBA écartée (trop peu de joueurs) | à valider |
| Cible | Note globale (OVR), valeur marchande, Ballon d'Or, poste, passe seule, plusieurs stats | Plusieurs stats principales prédites à partir d'autres stats. OVR écartée (calculée à partir des autres stats). Valeur marchande impossible (absente du CSV). Ballon d'Or écarté (trop peu de gagnants) | à valider |
| Entrées du modèle | Toutes les colonnes, sous-stats incluses | Stats principales + variables catégorielles, sans OVR ni sous-stats, pour éviter que le modèle triche | à valider |
| Gardiens | Les garder, les retirer | Retirés : leurs colonnes (GK Diving, etc.) sont vides pour les autres joueurs | à valider |
| Métrique | RMSE, R² | RMSE (en points de stat) et R², référence = prédire la moyenne | à valider |
| Modèle | Régression linéaire, forêt aléatoire | Forêt aléatoire (gère plusieurs sorties et donne l'importance des variables) | à valider |
| Technologie d'interface | Tkinter, Streamlit | Streamlit | à valider |