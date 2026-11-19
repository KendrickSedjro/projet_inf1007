L'IA a été utilisé pour le debugage et pour générer le code de certaines fonctionnalités, exemple pour compléter le fichier txt requirements, certains fichiers test, le readme, une partie du code d'interface et des fonctionnalités du  modele notamment pour les notions qui nécessite des connaisssance hors cours, c'est utile pour avoir un base code que l'on peut modifier 

| Outil | Demande | Réponse | Vérification | Décision |
|---|---|---|---|---|
| Claude (Timoty) | Prédire le poste, c'est faisable ? | Oui, ~86 % avec 4 groupes | Test rapide sur le CSV | Rejeté, on a préféré les stats |
| Claude (Timoty) | La passe est-elle corrélée aux autres stats ? | Plutôt oui | Test sur le CSV : PAS/DRI à 0,86, mais c'est la formule d'EA | Gardé, comme limite à expliquer |
| Claude (Timoty) | Pourquoi les .pyc revenaient dans Git | Le .gitignore était en UTF-16, donc ignoré par Git | Vérifié dans VS Code, converti en UTF-8, `git rm --cached` | Modifié |


Consignes :
Au moins 5 entrées, même si vous n'avez presque pas utilisé d'IA (dans ce cas, dites
le). Au moins une entrée montre une vérification qui a changé votre décision.
Colonnes  Outil · Ce que vous avez demandé · Réponse reçue · Vérification faite
(documentation, test, exécution) · Décision (gardé, modifié, rejeté).