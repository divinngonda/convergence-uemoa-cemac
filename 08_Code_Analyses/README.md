# Reproduire les analyses statistiques

Ce dossier contient le code Python utilisé pour recalculer les comparaisons de croissance et les analyses de convergence présentées dans `06_Documentation/`.

## Préparer Python

Installe Python 3.12 ou une version compatible, puis ouvre un terminal à la racine du dépôt. Crée un environnement isolé pour ce projet :

```bash
python -m venv .venv
```

Active-le selon ton système :

```bash
# macOS ou Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installe les bibliothèques requises et lance l'analyse :

```bash
python -m pip install -r 08_Code_Analyses/requirements.txt
python 08_Code_Analyses/analyses_statistiques.py
```

Le script utilise [pandas](https://pypi.org/project/pandas/) pour lire et joindre les tables, [NumPy](https://pypi.org/project/numpy/) pour les calculs numériques et les rééchantillonnages, [SciPy](https://pypi.org/project/scipy/) pour les tests statistiques, et [statsmodels](https://pypi.org/project/statsmodels/) pour les régressions. `requirements.txt` donne des plages de versions compatibles plutôt que des versions exactes; le code fixe cependant la graine et le nombre de tirages du bootstrap.

Le script lit `02_Donnees_Nettoyees/dim_pays.csv` et `fact_indicateurs.csv`. Il vérifie les colonnes, les doublons, les valeurs manquantes, les PIB par habitant positifs et la couverture attendue de 14 pays sur 2015–2025. Les résultats CSV sont écrits dans `07_Resultats_Analyses/`. Il remplace les deux CSV existants de convergence par les calculs correspondants et crée quatre nouveaux tableaux de résultats; les fichiers Excel sont laissés tels quels.

## Ce que le script calcule

- **Croissance :** test t de Welch et intervalle de confiance sur les moyennes nationales; permutation exacte et Mann–Whitney; comparaison complémentaire des observations annuelles avec effets fixes d'année et erreurs standards regroupées par pays.
- **β-convergence :** régression de la croissance annualisée du logarithme du PIB par habitant sur son niveau initial; tests classiques et HC3, corrélation de Spearman, permutation exacte et calculs « un pays retiré à la fois ».
- **σ-convergence :** écart-type population du logarithme du PIB par habitant par année et par zone; intervalle de confiance bootstrap apparié entre 2015 et 2025 (20 000 rééchantillonnages, graine fixe); analyse de sensibilité sans la Guinée équatoriale pour la CEMAC.

Les tests sont exploratoires : les groupes ne sont pas tirés au hasard, le nombre de pays est faible et les résultats ne démontrent pas un effet causal de l'appartenance à une zone.

## Fichiers produits

- `beta_convergence_uemoa_cemac.csv` : niveau initial et croissance annualisée par pays.
- `beta_regressions.csv` : résultats des régressions et tests par zone.
- `beta_sensibilite.csv` : pente estimée après retrait successif de chaque pays.
- `sigma_convergence_uemoa_cemac.csv` : dispersion annuelle par zone.
- `sigma_sensibilite.csv` : variation entre 2015 et 2025, intervalle bootstrap et sensibilité.
- `tests_croissance.csv` : résultats des comparaisons de croissance.

Les fichiers Excel présents dans `07_Resultats_Analyses/` sont conservés comme livrables complémentaires; ce script régénère les CSV.
