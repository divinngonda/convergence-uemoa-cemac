# Analyse de la convergence économique dans les espaces UEMOA et CEMAC (2015-2025)

## 1. Présentation du projet

Ce projet porte sur l'analyse comparative des dynamiques de croissance économique et de convergence des pays membres de l'Union économique et monétaire ouest-africaine (UEMOA) et de la Communauté économique et monétaire de l'Afrique centrale (CEMAC) entre 2015 et 2025.

L'étude vise à comparer les performances économiques des deux zones, à examiner les différences entre leurs pays membres et à déterminer si les écarts de PIB réel par habitant ont tendance à se réduire ou à s'accroître.

La démarche mobilise plusieurs outils de Data Analysis, depuis le nettoyage et la structuration des données jusqu'à leur exploitation dans MySQL, leur analyse statistique et leur visualisation avec Power BI.

## 2. Problématique

Dans quelle mesure les économies de l'UEMOA et de la CEMAC ont-elles convergé entre 2015 et 2025, et quelles différences de dynamique économique apparaissent entre les deux zones ?

## 3. Objectifs

- Comparer les performances de croissance économique de l'UEMOA et de la CEMAC.
- Identifier les écarts de performance entre les pays membres.
- Mesurer la dispersion des taux de croissance au sein de chaque zone.
- Étudier la σ-convergence à partir de la dispersion du logarithme du PIB réel par habitant.
- Étudier la β-convergence afin d'identifier d'éventuels mécanismes de rattrapage économique.
- Comparer les trajectoires économiques des deux unions monétaires.
- Présenter les principaux résultats de l'analyse dans un tableau de bord interactif.

## 4. Périmètre de l'étude

### UEMOA

- Bénin
- Burkina Faso
- Côte d'Ivoire
- Guinée-Bissau
- Mali
- Niger
- Sénégal
- Togo

### CEMAC

- Cameroun
- République centrafricaine
- République du Congo
- Gabon
- Guinée équatoriale
- Tchad

**Période étudiée : 2015-2025**

L'échantillon comprend 14 pays observés sur 11 années, soit **154 observations pays-année**.

## 5. Données utilisées

Les données proviennent de la base [World Development Indicators (WDI)](https://databank.worldbank.org/source/world-development-indicators) de la Banque mondiale. Les fichiers sources originaux sont conservés dans le dossier `01_Raw/`, puis transformés et harmonisés avant leur intégration dans MySQL.

Les deux indicateurs économiques principaux sont :

| Indicateur | Code WDI | Utilisation |
|---|---|---|
| Croissance annuelle du PIB réel | `NY.GDP.MKTP.KD.ZG` | Comparaison des performances de croissance |
| PIB réel par habitant, en dollars constants de 2015 | `NY.GDP.PCAP.KD` | Analyse de la convergence économique |

Le PIB réel par habitant est exprimé en dollars américains constants de 2015. Il s'agit d'un indicateur en prix constants, et non d'une mesure en parité de pouvoir d'achat.

## 6. Méthodologie

L'analyse suit plusieurs étapes complémentaires.

### 6.1. Préparation et contrôle des données

1. Extraction des données économiques depuis la Banque mondiale.
2. Nettoyage et transformation avec Power Query.
3. Harmonisation des formats et des variables.
4. Importation et structuration des données dans MySQL.
5. Contrôle de la qualité des données.

Les contrôles effectués sur le jeu de données final confirment :

- 154 observations pays-année ;
- 14 pays ;
- aucune valeur manquante pour les deux indicateurs principaux ;
- aucun doublon pays-année ;
- aucune valeur nulle ou négative pour le PIB réel par habitant.

### 6.2. Analyse de la croissance économique

Les analyses portent sur :

- la croissance moyenne par pays et par zone ;
- l'évolution annuelle des taux de croissance ;
- la dispersion des taux de croissance au sein de chaque zone ;
- la comparaison des performances entre les pays membres.

Les moyennes de croissance présentées dans cette étude sont des moyennes simples des taux nationaux. Elles ne constituent pas des agrégats régionaux pondérés par le poids économique de chaque pays.

### 6.3. Analyse de la σ-convergence

La σ-convergence est étudiée à partir de l'évolution de la dispersion du logarithme du PIB réel par habitant entre les pays d'une même zone.

Une diminution de cette dispersion peut indiquer un rapprochement des niveaux de PIB réel par habitant. Toutefois, cette évolution doit être interprétée avec prudence : elle ne signifie pas nécessairement que les pays les moins riches rattrapent les plus riches.

L'analyse prend également en compte la sensibilité des résultats à la présence de certains pays et un intervalle de confiance obtenu par bootstrap.

### 6.4. Analyse de la β-convergence

La β-convergence est étudiée à partir de la relation entre :

- le niveau initial de PIB réel par habitant en 2015 ;
- la croissance annualisée du logarithme du PIB réel par habitant entre 2015 et 2025.

Une relation négative entre le niveau initial et la croissance ultérieure peut suggérer un mécanisme de rattrapage.

Les coefficients sont accompagnés de tests de significativité, d'intervalles de confiance et de vérifications de sensibilité. Leur interprétation tient compte du faible nombre de pays dans chaque zone.

### 6.5. Préparation et visualisation

Les données sont également exploitées avec Excel pour certaines vérifications, analyses et préparations complémentaires.

Power BI est utilisé pour construire un tableau de bord interactif consacré à la comparaison des performances économiques des deux zones et de leurs pays membres.

Le tableau de bord est principalement centré sur la croissance : indicateurs synthétiques, comparaison des moyennes par zone, performances par pays, évolution annuelle et représentation géographique.

Les analyses statistiques détaillées de σ-convergence et de β-convergence sont présentées dans la documentation et les fichiers d'analyse associés au projet.

## 7. Principaux résultats

### 7.1. Croissance économique

Sur la période 2015-2025, les moyennes simples des taux de croissance nationaux sont les suivantes :

- **UEMOA : 5,27 %**
- **CEMAC : 0,86 %**

L'écart entre les deux zones est de l'ordre de 4,41 points de pourcentage.

La dispersion annuelle moyenne des taux de croissance est également plus faible dans l'UEMOA :

- **UEMOA : 1,45 point**
- **CEMAC : 3,31 points**

Ces résultats indiquent des performances de croissance plus élevées et des trajectoires nationales moins dispersées dans l'UEMOA sur la période étudiée.

### 7.2. σ-convergence

La dispersion du logarithme du PIB réel par habitant évolue comme suit :

- **CEMAC : 1,1100 à 0,9488**
- **UEMOA : 0,3892 à 0,4234**

La dispersion diminue en CEMAC et augmente légèrement dans l'UEMOA.

Cependant, la baisse observée en CEMAC reste fragile : l'intervalle de confiance du bootstrap inclut zéro et le retrait de la Guinée équatoriale réduit fortement la diminution constatée.

Ces résultats ne permettent donc pas d'affirmer qu'un processus robuste de σ-convergence est établi dans la CEMAC. Dans l'UEMOA, la légère hausse de dispersion ne suffit pas non plus à démontrer une divergence économique généralisée.

L'UEMOA conserve des niveaux de PIB réel par habitant nettement plus homogènes que la CEMAC.

### 7.3. β-convergence

Les régressions entre le niveau initial de PIB réel par habitant et sa croissance annualisée donnent les résultats suivants.

**CEMAC**

- β = **-1,646**
- R² = **0,453**
- Valeur p classique = **0,143**
- Nombre de pays : 6

Le coefficient négatif est compatible avec une relation de rattrapage, mais il n'est pas statistiquement significatif au seuil de 5 %. Les tests complémentaires ne permettent pas de confirmer cette relation.

**UEMOA**

- β = **+0,771**
- R² = **0,204**
- Valeur p classique = **0,262**
- Nombre de pays : 8

Le coefficient positif ne met pas en évidence de mécanisme de rattrapage. Il n'est toutefois pas statistiquement significatif non plus. Un test de sensibilité HC3 donne une valeur p différente (0,024), mais les autres vérifications ne confirment pas ce résultat.

**Bilan :** les estimations ne permettent pas de conclure à une β-convergence statistiquement établie dans l'une ou l'autre des deux zones.

## 8. Interprétation générale

Les deux zones présentent des trajectoires économiques différentes.

L'UEMOA affiche une croissance moyenne supérieure à celle de la CEMAC et une dispersion des taux de croissance plus faible. Elle présente également des niveaux de PIB réel par habitant plus homogènes.

En CEMAC, la dispersion du PIB réel par habitant diminue entre 2015 et 2025. Cette évolution doit néanmoins être nuancée : elle dépend fortement de la trajectoire de certains pays, notamment la Guinée équatoriale. La baisse de dispersion ne correspond donc pas nécessairement à un rattrapage généralisé des économies les moins riches.

Les estimations de β-convergence ne permettent pas de confirmer statistiquement un mécanisme de rattrapage dans les deux zones.

Dans l'ensemble, les résultats mettent en évidence un écart de performance économique entre l'UEMOA et la CEMAC, mais ne permettent pas d'établir l'existence d'un processus robuste de convergence économique sur la période étudiée.

## 9. Outils utilisés

- **Power Query** : nettoyage et transformation des données.
- **MySQL / MySQL Workbench** : stockage, structuration, jointures et analyses SQL.
- **Excel** : vérifications, analyses et préparation complémentaire des données.
- **Python** : audit statistique, recalculs et analyses de sensibilité.
- **Power BI** : création du tableau de bord interactif et visualisation des résultats.
- **VS Code** : contrôle des fichiers CSV et rédaction de la documentation Markdown.

## 10. Limites de l'analyse

Cette étude constitue une analyse exploratoire portant sur 14 pays et une période de onze années.

Plusieurs limites doivent être prises en compte :

- Le faible nombre de pays dans chaque zone réduit la puissance des tests statistiques.
- Les économies étudiées peuvent être exposées à des chocs communs, ce qui limite certaines hypothèses d'indépendance.
- Les résultats de β-convergence ne sont statistiquement significatifs dans aucune des deux zones selon les régressions classiques.
- La baisse de dispersion observée en CEMAC est sensible à la présence de certains pays, notamment la Guinée équatoriale.
- Les moyennes de croissance sont des moyennes simples et non des agrégats pondérés par le PIB.
- Les résultats portent sur la croissance et le PIB réel par habitant. Ils ne prennent pas en compte l'ensemble des facteurs institutionnels, sociaux, démographiques et structurels susceptibles d'influencer les trajectoires économiques nationales.

Ces limites invitent à considérer les résultats comme des éléments de comparaison et d'analyse, plutôt que comme des conclusions définitives sur la convergence à long terme.

## 11. Documentation et structure du projet

Les trois documents de référence sont conservés dans `06_Docs/` :

- [README du projet](README_Projet.md)
- [Analyse exploratoire](Analyse_Exploratoire.md)
- [Conclusions](Conclusions.md)

Arborescence générale :

Projet_Convergence_UEMOA_CEMAC/
│
├── 01_Donnees_Brutes/
│   ├── API_NY.GDP.PCAP.KD_DS2_en_csv_v2_380.csv
│   └── API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_57.csv
│
├── 02_Donnees_Nettoyees/
│   ├── pib_reel_par_habitant_uemoa_cemac.nettoye.csv
│   ├── croissance_pib_uemoa_cemac.csv
│   ├── croissance_pib_uemoa_cemac_nettoye.xlsx
│   ├── dim_pays.csv
│   ├── fact_indicateurs.csv
│   └── modele_powerbi_uemoa_cemac.xlsx
│
├── 03_Base_MySQL/
│   ├── 01_creation_base.sql
│   ├── 02_creation_tables.sql
│   ├── 03_insertion_pays.sql
│   └── 04_import_donnees.sql
│
├── 04_Requetes_SQL/
│   ├── 05_requetes_analyse.sql
│   └── 06_export_powerbi.sql
│
├── 05_Dashboard_PowerBI/
│   ├── 01_Livrable_Final/
│   │   └── uemoa_cemac_dashboard_final.pbix
│   │
│   ├── 02_Projet_PowerBI/
│   │   ├── uemoa_cemac_dashboard.Report/
│   │   ├── uemoa_cemac_dashboard.SemanticModel/
│   │   └── uemoa_cemac_dashboard.pbip
│   │
│   └── README_Dashboard.md
│
├── 06_Documentation/
│   ├── Analyse_Exploratoire.md
│   ├── Conclusions.md
│   └── README_Projet.md
│
└── 07_Resultats_Analyses/
    ├── beta_convergence_uemoa_cemac.csv
    ├── beta_convergence_uemoa_cemac.xlsx
    ├── sigma_convergence_uemoa_cemac.csv
    └── sigma_convergence_uemoa_cemac.xlsx

Cette arborescence présente l'organisation générale du projet. Les fichiers sources, les données nettoyées, les scripts SQL, le fichier Power BI et les documents de référence doivent être conservés dans leurs dossiers respectifs.

## 12. Sources des données

**Banque mondiale — World Development Indicators (WDI)**

- [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)
- [Croissance annuelle du PIB — NY.GDP.MKTP.KD.ZG](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG)
- [PIB réel par habitant, dollars constants de 2015 — NY.GDP.PCAP.KD](https://data.worldbank.org/indicator/NY.GDP.PCAP.KD)

Les données et les résultats doivent être interprétés en tenant compte des éventuelles révisions de la base WDI.

