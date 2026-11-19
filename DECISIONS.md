# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Sport, immobilier | Sport (football) : on connaît le domaine, ce qui permet de juger si les résultats ont du sens | à valider |
| Jeu de données | Kaggle EA FC 25 (stats de joueurs), NBA 2026 | EA FC 25 : 17 737 joueurs, licence Apache 2.0 vérifiée sur Kaggle. NBA écartée (trop peu de joueurs) | à valider |
| Cible | Note globale (OVR), valeur marchande, Ballon d'Or, poste, une seule stat, plusieurs stats | Les 6 stats principales (PAC, SHO, PAS, DRI, DEF, PHY). OVR écartée (calculée à partir des autres stats). Valeur marchande impossible (absente du CSV, vérifié en ouvrant le fichier). Ballon d'Or écarté (trop peu de gagnants). Poste jugé faisable (~86 % avec 4 groupes) mais l'équipe a préféré les stats | à valider |
| Entrées du modèle | Toutes les colonnes, stats principales, sous-stats | Sous-stats numériques (Acceleration, Sprint Speed, Positioning, Shot Power, Long Shots, Volleys, Penalties, Vision, Crossing) et pied fort. Limite connue : ces sous-stats composent PAC, SHO et PAS | à valider |
| Variable catégorielle | Position, pied fort | Pied fort, encodé 0 (gauche) / 1 (droit) pour l'entraînement | à valider |
| Gardiens | Les garder, les retirer | Retirés : leurs colonnes (GK Diving, etc.) sont vides pour les autres joueurs | à valider |
| Métrique | RMSE, R² | RMSE (en points de stat) et R², comparés à la référence « prédire la moyenne » | à valider |
| Modèle | Régression linéaire, forêt aléatoire | Forêt aléatoire à plusieurs sorties (une pour chaque stat) | à valider |
| Technologie d'interface | Tkinter, Streamlit | Streamlit | à valider |
| Saisie dans l'interface | Champs manuels pour chaque entrée, recherche d'un joueur par son nom | Recherche par nom, qui compare stats réelles et prédites. Écart connu avec la consigne (un champ par variable d'entrée) | à valider |
| Données personnelles | Retirer la colonne des noms, la garder | Colonne gardée : ce sont des joueurs professionnels (informations publiques) et l'interface s'en sert. À faire confirmer par l'auxiliaire | à valider |