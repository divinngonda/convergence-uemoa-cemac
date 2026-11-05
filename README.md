# Analyse de la convergence économique : UEMOA vs CEMAC (2015–2025)

## Présentation du projet

Ce projet analyse les dynamiques de croissance économique et de convergence entre les pays membres de l'Union économique et monétaire ouest-africaine (UEMOA) et de la Communauté économique et monétaire de l'Afrique centrale (CEMAC) sur la période 2015–2025.

L'objectif est de comparer les performances économiques des deux espaces, d'étudier les disparités entre pays et d'examiner si les économies tendent à se rapprocher en matière de niveau de vie.

## Périmètre et données

- **Période :** 2015–2025
- **Pays étudiés :** 14 pays (8 UEMOA et 6 CEMAC)
- **Observations :** 154
- **Source principale :** Banque mondiale – World Development Indicators (WDI)

Indicateurs étudiés :
- Croissance annuelle du PIB (%).
- PIB par habitant en dollars constants de 2015.

## Outils utilisés

- **Excel :** exploration, préparation et contrôle des données.
- **MySQL :** structuration de la base de données et requêtes SQL.
- **Power BI :** analyse exploratoire et visualisation interactive.

## Principaux résultats

- La croissance annuelle moyenne du PIB atteint **5,27 % dans l'UEMOA**, contre **0,86 % dans la CEMAC**.
- L'écart moyen entre les deux espaces est de **4,41 points de pourcentage**.
- La dispersion des taux de croissance est plus importante dans la CEMAC (écart-type de 3,31 contre 1,45 dans l'UEMOA).
- L'analyse de convergence bêta ne permet pas d'établir statistiquement une convergence des pays dans l'un ou l'autre espace.
- Les résultats de convergence sigma sont contrastés et doivent être interprétés avec prudence.

*Les moyennes de croissance présentées sont des moyennes simples entre pays, et non des moyennes pondérées par le PIB.*

## Organisation du projet

| Dossier | Contenu |
|---|---|
| `01_Donnees_Brutes` | Données sources |
| `02_Donnees_Nettoyees` | Données préparées et nettoyées |
| `03_Base_MYSQL` | Scripts de création et de gestion de la base |
| `04_Requetes_SQL` | Requêtes d'analyse |
| `05_Dashboard_PowerBI` | Dashboard et fichiers du projet Power BI |
| `06_Documentation` | Documentation et méthodologie |
| `07_Resultats_Analyses` | Résultats et analyses complémentaires |

## Livrables et documentation

- [Documentation détaillée du projet](06_Documentation/README_Projet.md)
- [Documentation du dashboard Power BI](05_Dashboard_PowerBI/README_Dashboard.md)
- [Dashboard Power BI – fichier PBIX](05_Dashboard_PowerBI/01_Livrable_Final/uemoa_cemac_dashboard_final.pbix)
- [Projet Power BI modifiable](05_Dashboard_PowerBI/02_Projet_PowerBI/)

## Source des données

Banque mondiale – [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)

---

**Projet personnel de portfolio – Data Analysis**

*Analyse, traitement, requêtage et visualisation de données économiques.*
