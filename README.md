# ⚽ FootPredictor

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Machine Learning" src="https://img.shields.io/badge/ML-Modeling-FF6B35?style=for-the-badge">
  <img alt="Data" src="https://img.shields.io/badge/Data-CSV-34A853?style=for-the-badge">
  <img alt="App" src="https://img.shields.io/badge/GUI-Streamlit%20%2F%20Tkinter-8B5CF6?style=for-the-badge">
</p>

<p align="center">
  <strong>Projet de data science • football • IA • interface locale</strong>
</p>

> Un projet de machine learning appliqué au football : analyse d’un dataset de joueurs, entraînement d’un modèle simple et développement d’une interface de prédiction locale.

## 🧭 Objectif général

Ce projet s’inscrit dans une démarche professionnelle de data science. L’objectif est de créer une application complète qui permet de :

- explorer un jeu de données football ;
- nettoyer et structurer les variables ;
- choisir une cible de prédiction pertinente ;
- entraîner et évaluer un modèle simple ;
- présenter un résultat de façon claire dans une interface locale.

<table>
  <tr>
    <td align="center"><h3>📊</h3><b>Jeu de données</b><br>CSV, variables, nettoyage</td>
    <td align="center"><h3>🧠</h3><b>Modèle</b><br>Régression / classification</td>
    <td align="center"><h3>🖥️</h3><b>Interface</b><br>Prédiction + historique</td>
  </tr>
</table>

## 👥 Modalités

- Équipe : binôme de 2 étudiants
- Durée estimée : environ 8 heures
- Évaluation : priorité donnée à la démarche, à la qualité du travail et à la clarté de l’analyse
- Livrables principaux :
  - dépôt GitHub public
  - README complet
  - fiche de décisions (`DECISIONS.md`)
  - journal IA (`JOURNAL_IA.md`)
  - présentation orale de 10 minutes

## 🏟️ Les trois volets du projet

### 1) Jeu de données

Domaine libre : santé, sport, immobilier, transport, éducation, etc.

Critères techniques :

- format CSV tabulaire
- 500 à 50 000 lignes
- au moins 5 colonnes d’entrée
- variable cible : catégorie ou valeur numérique
- au moins une variable numérique et une variable catégorielle

Exclusions strictes :

- Iris
- Titanic
- MNIST
- données personnelles identifiables

### 2) Entraîner un modèle simple

Modèles autorisés :

- régression linéaire ou logistique
- KNN
- arbre de décision
- forêt aléatoire

Étapes clés :

- explorer et nettoyer les données
- choisir une métrique adaptée
- séparer les données en train/test avec graine fixe
- créer une référence simple
- entraîner et évaluer le modèle honnêtement
- sauvegarder le modèle et les métadonnées

### 3) Interface graphique

Technologies autorisées :

- Tkinter
- PyQt / PySide
- Streamlit
- Gradio

Fonctionnalités minimales :

- saisie des caractéristiques selon le type de variables
- validation des entrées sans traceback
- bouton “Prédire” avec résultat clair
- au moins un graphique Matplotlib
- historique des prédictions sauvegardé
- avertissement si le domaine est sensible

## ✅ Exigences d'implémentation

| Chapitre | Exigences |
|---|---|
| E/S | Lecture/écriture de fichiers, gestion des chemins, blocs `with` |
| Fonctions | Fonctions courtes, docstrings, annotations de type |
| Modules | Au moins 4 modules (`donnees.py`, `modele.py`, `exceptions.py`, `interface.py`) + `main.py` |
| Exceptions / Tests / CI | Exceptions personnalisées, 8 tests `pytest`, couverture, workflow GitHub Actions |
| POO | Au moins 3 classes, encapsulation, héritage/polymorphisme, composition |
| NumPy | Au moins un calcul vectorisé |
| Matplotlib / IA | Graphes, documentation officielle, journal d’IA critique |

## 🧪 Jalons de validation

- Validation A : domaine choisi
- Validation B : jeu de données validé
- Validation C : variable cible, métrique et modèle retenus
- Validation D : technologie d’interface choisie et maquette papier

## 📊 Barème d’évaluation global (/100)

| Critère | Points |
|---|---:|
| Jeu de données et problème | 10 |
| Modèle | 15 |
| Interface graphique | 20 |
| Conception et qualité du code | 20 |
| Tests, Git et CI | 10 |
| Justification des choix et usage de l’IA | 10 |
| Présentation et questions | 15 |

## 🏁 Résumé

Le projet combine trois compétences essentielles :

- analyse de données ;
- modélisation machine learning ;
- conception d’une interface utilisateur fonctionnelle.

L’enjeu est surtout la qualité de la démarche et de l’interprétation, pas seulement la performance brute du modèle.

---

<p align="center">
  <b>🔥 Ready to build ?</b>
</p>
