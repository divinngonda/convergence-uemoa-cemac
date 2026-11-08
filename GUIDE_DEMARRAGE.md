# Guide de démarrage et de publication

Ce guide décrit comment récupérer le projet, reproduire ses analyses et préparer une modification GitHub. Les commandes sont écrites pour être lancées une à la fois dans un terminal, à la racine du dossier du projet.

## 1. Git et GitHub, en deux phrases

- **Git** garde l'historique des versions sur ton ordinateur. Il permet de voir ce qui a changé et de revenir sur une modification.
- **GitHub** héberge une copie en ligne que les recruteurs peuvent consulter. Envoyer tes changements sur GitHub s'appelle un *push*; intégrer une proposition dans la version principale s'appelle une *fusion* (*merge*).

Une modification ne part pas automatiquement sur GitHub : elle reste d'abord sur ton ordinateur, puis elle est enregistrée (*commit*) et envoyée (*push*) quand tu le décides.

## 2. Récupérer le projet

La première fois, ouvre le terminal et place-toi dans le dossier où tu veux garder le projet. Puis lance :

```bash
git clone https://github.com/divinngonda/convergence-uemoa-cemac.git
cd convergence-uemoa-cemac
```

La première commande télécharge le dépôt GitHub et son historique. La seconde entre dans le dossier téléchargé. Pour revenir plus tard et prendre les changements publiés depuis ta dernière visite :

```bash
cd chemin/vers/convergence-uemoa-cemac
git pull
```

`git status` résume l'état du dossier. `git diff` montre précisément les lignes modifiées :

```bash
git status
git diff
```

## 3. Reproduire les analyses Python

Le script utilise les deux fichiers nettoyés du dossier `02_Donnees_Nettoyees/`. Depuis la racine du projet, crée un environnement Python séparé, active-le, installe les bibliothèques, puis lance le script.

```bash
python -m venv .venv
```

Activation dans le terminal macOS/Linux :

```bash
source .venv/bin/activate
```

Activation dans Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Installation et lancement :

```bash
python -m pip install -r 08_Code_Analyses/requirements.txt
python 08_Code_Analyses/analyses_statistiques.py
```

Le script écrit les résultats CSV dans `07_Resultats_Analyses/`. Il recalcule les moyennes nationales, les tests de comparaison, les pentes de β-convergence, les dispersions de σ-convergence, le bootstrap et les analyses de sensibilité. Les méthodes et leurs limites sont expliquées dans [le guide du code](08_Code_Analyses/README.md).

Pour quitter l'environnement Python quand tu as fini :

```bash
deactivate
```

## 4. Recréer la base MySQL (étape facultative)

Si tu veux reproduire la partie SQL, crée la base en exécutant les scripts numérotés de `03_Base_MYSQL/` dans cet ordre :

1. `01_creation_base.sql`
2. `02_creation_tables.sql`
3. `03_insertion_pays.sql`
4. `04_creation_tables_import.sql`

Ce script prépare les tables de réception. Ensuite, utilise l'assistant **Table Data Import Wizard** de MySQL Workbench pour importer `croissance_pib_uemoa_cemac.csv` dans `croissance_pib_import` et `pib_reel_par_habitant_uemoa_cemac.nettoye.csv` dans `pib_reel_par_habitant_import`. Ces fichiers sont séparés par des points-virgules (`;`) et ont une ligne d'en-tête; vérifie le séparateur et l'ordre des quatre colonnes dans l'assistant.

Après les deux imports, exécute `05_import_donnees.sql` pour transférer les valeurs dans la table principale et effectuer les contrôles. Les requêtes d'analyse se trouvent ensuite dans `04_Requetes_SQL/05_requetes_analyse.sql`.

## 5. Ouvrir ou actualiser le tableau de bord

- Pour consulter la version finale, ouvre `05_Dashboard_PowerBI/01_Livrable_Final/uemoa_cemac_dashboard_final.pbix` dans Power BI Desktop.
- Pour voir les requêtes et modifier le projet, ouvre `05_Dashboard_PowerBI/02_Projet_PowerBI/uemoa_cemac_dashboard.pbip`.
- Pour actualiser le projet modifiable, il faut une connexion Internet. Si Power BI demande les identifiants de la source Web GitHub, choisis **Anonyme**; si l'application demande un niveau de confidentialité, choisis **Public**.

Power BI Desktop est disponible pour Windows selon les [prérequis Microsoft](https://learn.microsoft.com/fr-fr/power-bi/fundamentals/desktop-get-the-desktop). Pour une connexion Web publique, Microsoft distingue le type d'authentification **Anonyme** du niveau de confidentialité **Public**; consulte [la documentation Microsoft sur le connecteur Web](https://learn.microsoft.com/en-us/power-query/connectors/web/web) si les fenêtres de connexion diffèrent. Le fichier `.pbix` est le rapport prêt à consulter; le dossier `.pbip` contient le projet éditable et ses requêtes.

## 6. Comprendre la date des données

Les fichiers couvrent les années 2015 à 2025. Le fichier WDI de croissance conservé dans `01_Donnees_Brutes/` indique **Last Updated Date: 2026-07-13**. Cette date est celle de la dernière mise à jour WDI indiquée dans le fichier, pas la date à laquelle le fichier a été téléchargé. Le fichier du PIB réel par habitant ne conserve pas cette métadonnée; sa date d'extraction n'est donc pas connue à partir des éléments publiés.

WDI peut réviser les séries historiques. Pour refaire l'analyse avec une nouvelle extraction, conserve une copie de la source, note la date de téléchargement, mets à jour les tables propres, puis actualise les résultats et le modèle Power BI.

## 7. Publier une modification avec Git

Pour une amélioration, crée d'abord une branche séparée. Une branche est un espace de travail nommé qui permet de préparer une modification sans toucher immédiatement à la version principale (`main`).

```bash
git switch -c amelioration-portfolio
```

Après tes modifications, regarde ce qui va être enregistré :

```bash
git status
git diff
git diff --check
```

Choisis les fichiers à inclure avec `git add`, puis crée un commit avec un message qui résume l'objectif :

```bash
git add README.md GUIDE_DEMARRAGE.md 03_Base_MYSQL 05_Dashboard_PowerBI 06_Documentation 08_Code_Analyses
git commit -m "Ameliorer la reproductibilite du projet"
```

Un *commit* est un point de sauvegarde local avec une description. Il n'est pas encore publié. Pour envoyer la branche sur GitHub :

```bash
git push -u origin amelioration-portfolio
```

Sur GitHub, ouvre ensuite une **Pull request** pour comparer la branche à `main`, relire le changement et demander sa fusion. Une Pull request est une proposition de modification; la fusion est l'étape qui l'intègre à la version principale visible sur le dépôt. Le *push* publie la branche sur GitHub, mais `main` ne change qu'après la fusion. Pour remettre ton dossier local à jour après la fusion :

```bash
git switch main
git pull
```

Pour un petit projet personnel, tu peux aussi pousser directement sur `main`, mais une branche et une Pull request créent une étape de relecture utile.

## 8. Résumé des commandes Git

| Commande | Ce qu'elle fait |
|---|---|
| `git clone URL` | Télécharge le dépôt et son historique sur ton ordinateur. |
| `git pull` | Récupère les changements publiés depuis la dernière synchronisation. |
| `git status` | Indique quels fichiers sont modifiés ou prêts à être enregistrés. |
| `git diff` | Affiche les différences de contenu. |
| `git add fichier` | Sélectionne un fichier pour le prochain commit. |
| `git commit -m "message"` | Enregistre localement une version avec un message. |
| `git push` | Envoie les commits locaux vers GitHub. |

Garde ces étapes séparées au début : **modifier → examiner → sélectionner → enregistrer → publier**. Cela rend chaque changement plus facile à comprendre et à corriger.
