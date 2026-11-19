L'IA a été utilisé pour le debugage et pour générer le code de certaines fonctionnalités, exemple pour compléter le fichier txt requirements, certains fichiers test, le readme, une partie du code d'interface et des fonctionnalités du  modele notamment pour les notions qui nécessite des connaisssance hors cours, c'est utile pour avoir un base code que l'on peut modifier 

| Outil | Demande | Réponse | Vérification | Décision |
|---|---|---|---|---|
| Claude (Timoty) | Prédire le poste, c'est faisable ? | Oui, ~86 % avec 4 groupes | Test rapide sur le CSV | Rejeté, on a préféré les stats |
| Claude (Timoty) | La passe est-elle corrélée aux autres stats ? | Plutôt oui | Test sur le CSV : PAS/DRI à 0,86, mais c'est la formule d'EA | Gardé, comme limite à expliquer |
| Claude (Timoty) | Pourquoi les .pyc revenaient dans Git | Le .gitignore était en UTF-16, donc ignoré par Git | Vérifié dans VS Code, converti en UTF-8, `git rm --cached` | Modifié |
| Gemini (Kendrick) | Choisit le modèle le plus optimale pour notre jeux de données | Random forest et Decision tree | Recherche sur les modèles RF et DT | Choisit le random forest |
| Gemini (Kendrick) | Comment optimiser la précision (RMSE) du modele | Génération d'un pseudo code utilisant GridSearchCV une class de Sklearn  | Recherche sur le fonctionnement du GridSearch | Accepté, Garder le code |
| Gemini (Kendrick) | Génère un code pour le fichier test du modèle | Génération d'un pseudo code | Relecture du code et évaluation des edges cases | Accepté, Garder le code |
| Gemini (Kendrick) | Génère un pseudo code pour l'interface | créée un pseudo code | Lecture du code et recherche sur les méthodes utilisées | Accepté, Garder le code modification de la structure, implémentation des graphiques |