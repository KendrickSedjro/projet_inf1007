# ⚽ Projet
# FootPredictor

App Streamlit qui compare les stats réelles et prédites d'un joueur de football (EA FC 25). Projet 2 d'INF1007, fait par Timoty Paye et Kendrick Da Silva.

C'est un exercice de cours : le modèle retrouve en grande partie la formule qu'EA utilise pour calculer les notes, pas la réalité du football.

## Données

Source : « EA SPORTS FC 25 Database, Ratings and Stats » (nyagami) sur Kaggle, licence Apache 2.0 : https://www.kaggle.com/datasets/nyagami/ea-sports-fc-25-database-ratings-and-stats

Le CSV (5,5 Mo) est dans `donnees/raw/`. Il y a 17 737 joueurs, 15 738 une fois les gardiens retirés (leurs colonnes GK sont vides pour les autres). Après nettoyage, il ne manque aucune valeur. Les noms sont ceux de joueurs pros, donc des infos publiques.

## Lancer le projet

```
git clone https://github.com/KendrickSedjro/projet_inf1007.git
cd projet_inf1007
pip install -r requirements.txt
python -m streamlit run src/interface.py
```

Le modèle est déjà entraîné et sauvegardé dans `model/`. Pour le refaire : `python src/model.py`.

## Où est quoi

- `src/donnees.py` : chargement, nettoyage, encodage du pied fort, classes `Variable`
- `src/model.py` : entraînement, comparaison avec la référence, sauvegarde
- `src/metriques.py` : RMSE et R² faits avec NumPy
- `src/historique.py` : historique des prédictions
- `src/exceptions.py` : `DonneeInvalideError`
- `src/exploration.py` : graphique d'exploration
- `src/interface.py` : l'app
- `tests/` : les tests pytest

## Le modèle

On prédit 6 stats (PAC, SHO, PAS, DRI, DEF, PHY) avec une forêt aléatoire. Les entrées sont 9 sous-stats (Acceleration, Sprint Speed, Positioning, Shot Power, Long Shots, Volleys, Penalties, Vision, Crossing) et le pied fort, codé 0 pour gauche et 1 pour droit. On compare au modèle trivial qui prédit toujours la moyenne.

| Stat | RMSE test | R² test | RMSE si on prédit la moyenne (≈) |
|---|---|---|---|
| PAC | 1,67 | 0,976 | 10,9 |
| SHO | 2,70 | 0,963 | 14,1 |
| PAS | 3,06 | 0,904 | 10,0 |
| DRI | 3,77 | 0,839 | 9,5 |
| DEF | 10,60 | 0,563 | 16,1 |
| PHY | 8,11 | 0,293 | 9,6 |

Les limites:
- Les sous-stats qu'on donne en entrée sont celles qu'EA utilise pour calculer PAC, SHO et PAS. Les bons scores viennent surtout de là.
- L'app cherche un joueur par son nom et compare ses stats. Elle n'a pas encore de champs pour saisir les variables une par une.

## Tests

35 tests pytest (cas normaux, limites, erreurs avec `pytest.raises`, `pytest.approx` pour les flottants). Nos RMSE et R² faits avec NumPy sont comparés à ceux de scikit-learn. Couverture mesurée avec `python -m coverage` : 62 % au total (donnees 92 %, historique 100 %, metriques 100 %, model 74 %, interface 0 %). La CI lance pytest à chaque push.

## Outil du chapitre 7

`lire_historique` trie les prédictions de la plus récente à la plus ancienne avec une `lambda` comme clé de tri.

## Documentation

pandas (https://pandas.pydata.org/docs/), scikit-learn (https://scikit-learn.org/stable/), Streamlit (https://docs.streamlit.io/).

Voir aussi `DECISIONS.md` et `JOURNAL_IA.md`.