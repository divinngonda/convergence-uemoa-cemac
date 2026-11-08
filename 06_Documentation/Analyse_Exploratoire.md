

# Analyse exploratoire

Les tests et analyses de sensibilité présentés ici sont reproductibles avec le [script Python](../08_Code_Analyses/analyses_statistiques.py); les étapes d'installation figurent dans le [guide du code](../08_Code_Analyses/README.md).

## 1. Croissance moyenne par zone (2015-2025)

### Résultats

- UEMOA : **5,27 %**
- CEMAC : **0,86 %**
- Écart entre les deux zones : **4,41 points de pourcentage**

### Interprétation

Entre 2015 et 2025, les pays de l'UEMOA ont enregistré une croissance moyenne du PIB réel nettement supérieure à celle des pays de la CEMAC.

L'écart entre les deux zones atteint environ 4,41 points de pourcentage. Cette différence traduit une dynamique de croissance plus soutenue au sein de l'UEMOA sur la période étudiée.

Ces résultats correspondent à des moyennes simples des taux de croissance nationaux : chaque pays a donc le même poids dans le calcul, quelle que soit la taille de son économie. Ils ne représentent pas des taux de croissance régionaux pondérés par le poids économique de chaque pays.

### Vérification statistique complémentaire

Pour examiner si l'écart observé dépasse une simple différence descriptive, les moyennes de croissance sur onze ans ont été comparées au niveau des pays : huit observations pour l'UEMOA et six pour la CEMAC.

Le test t de Welch donne une différence estimée de 4,405 points de pourcentage, avec une valeur p de 0,0158 et un intervalle de confiance à 95 % compris entre 1,22 et 7,59 points. Les tests exacts de permutation et de Mann-Whitney vont également dans le sens d'une différence entre les deux groupes.

Une vérification complémentaire utilisant les observations annuelles, avec effets fixes temporels et erreurs standards regroupées par pays, donne un écart estimé de 4,405 points (p = 0,0035). Cette estimation doit toutefois être interprétée avec prudence, car elle repose sur seulement quatorze pays.

Ces tests renforcent le constat d'un écart de croissance entre les deux groupes dans le cadre des méthodes utilisées. Ils ne démontrent pas que l'appartenance à une union monétaire est la cause de cet écart. Les quatorze pays représentent par ailleurs l'ensemble des membres des deux zones étudiées, et non un échantillon tiré au hasard.

Il serait également incorrect de traiter les 154 observations pays-année comme 154 observations indépendantes dans un test classique : les données d'un même pays sont suivies sur plusieurs années. Cela créerait un risque de pseudo-réplication et conduirait à sous-estimer l'incertitude statistique.

## 2. Performance économique par pays (2015-2025)

### Objectif

Analyser la croissance moyenne du PIB réel des pays de l'UEMOA et de la CEMAC afin d'identifier les différences de performance entre les économies membres.

### Requête SQL utilisée

```sql
SELECT
    p.zone,
    p.nom_pays,
    ROUND(AVG(i.croissance_pib), 2) AS croissance_moyenne
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
GROUP BY
    p.zone,
    p.nom_pays
ORDER BY
    p.zone,
    croissance_moyenne DESC;
```

### Résultats principaux

#### UEMOA

- Côte d'Ivoire : **6,06 %**
- Bénin : **5,77 %**
- Niger : **5,72 %**
- Sénégal : **5,46 %**
- Togo : **5,09 %**
- Guinée-Bissau : **4,87 %**
- Burkina Faso : **4,75 %**
- Mali : **4,41 %**

#### CEMAC

- Cameroun : **3,51 %**
- République centrafricaine : **2,69 %**
- Tchad : **2,48 %**
- Gabon : **2,02 %**
- République du Congo : **-1,07 %**
- Guinée équatoriale : **-4,45 %**

### Interprétation

Les résultats mettent en évidence des différences importantes entre les performances économiques des deux zones.

En UEMOA, les huit pays affichent une croissance moyenne supérieure à 4 %. La Côte d'Ivoire arrive en tête avec 6,06 %, suivie du Bénin (5,77 %) et du Niger (5,72 %). Les résultats restent relativement proches entre les pays, même si des écarts de performance subsistent.

La situation est plus contrastée en CEMAC. Le Cameroun affiche la croissance moyenne la plus élevée de la zone, avec 3,51 %. À l'autre extrémité, la République du Congo (-1,07 %) et la Guinée équatoriale (-4,45 %) présentent des moyennes négatives sur la période.

Cette différence de profils contribue à expliquer l'écart de croissance entre les deux zones. Elle montre également que la moyenne d'une zone peut masquer des trajectoires nationales très différentes, particulièrement en CEMAC.

Il faut toutefois distinguer une moyenne nationale négative sur onze années d'une baisse continue de l'activité économique : cet indicateur résume les taux annuels observés et ne décrit pas, à lui seul, l'évolution de chaque économie année après année.

## 3. Évolution annuelle de la croissance par zone

### Objectif

Analyser l'évolution de la croissance moyenne du PIB réel de l'UEMOA et de la CEMAC entre 2015 et 2025 afin d'identifier les différences de dynamique entre les deux zones.

### Requête SQL utilisée

```sql
SELECT
    i.annee,
    p.zone,
    ROUND(AVG(i.croissance_pib), 2) AS croissance_moyenne
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
GROUP BY
    i.annee,
    p.zone
ORDER BY
    i.annee,
    p.zone;
```

### Résultats principaux

Sur l'ensemble de la période 2015-2025, la croissance moyenne annuelle de l'UEMOA est supérieure à celle de la CEMAC chaque année.

La CEMAC enregistre notamment des taux de croissance moyens négatifs en 2016 (-1,71 %), 2017 (-0,72 %) et 2020 (-2,02 %).

L'UEMOA conserve une croissance positive sur l'ensemble de la période. Un ralentissement important est néanmoins observé en 2020, avec une croissance moyenne de 2,03 %, contre 5,68 % en 2019.

À partir de 2021, l'UEMOA retrouve des niveaux de croissance supérieurs à 5 % sur la plupart des années, pour atteindre 6,41 % en 2025.

### Interprétation

Les résultats montrent une dynamique de croissance plus soutenue au sein de l'UEMOA sur la période étudiée.

L'année 2020 constitue une rupture importante pour les deux zones. Le ralentissement de la croissance observé cette année-là est compatible avec l'effet d'un choc économique commun, dans un contexte marqué par la pandémie de Covid-19. Cette comparaison descriptive ne permet cependant pas d'isoler l'effet de la pandémie des autres facteurs économiques.

Les trajectoires de reprise sont différentes. L'UEMOA retrouve rapidement des taux de croissance élevés, tandis que la CEMAC connaît une reprise plus irrégulière et conserve des performances inférieures à celles de l'UEMOA.

Cette évolution confirme l'écart observé dans les moyennes sur l'ensemble de la période, tout en montrant que les différences entre les deux zones ne se limitent pas à une seule année.

## 4. Dispersion des taux de croissance au sein des zones

### Objectif

Mesurer l'hétérogénéité des taux de croissance entre les pays de chaque zone afin de déterminer si les performances économiques nationales sont relativement proches ou dispersées.

### Requête SQL utilisée

```sql
SELECT
    i.annee,
    p.zone,
    ROUND(AVG(i.croissance_pib), 2) AS croissance_moyenne,
    ROUND(STDDEV_POP(i.croissance_pib), 2) AS ecart_type
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
GROUP BY
    i.annee,
    p.zone
ORDER BY
    i.annee,
    p.zone;
```

### Résultats principaux

L'UEMOA présente généralement une dispersion des taux de croissance plus faible que la CEMAC.

Entre 2015 et 2019, l'écart-type de l'UEMOA diminue progressivement :

- 2015 : 1,63
- 2016 : 1,20
- 2017 : 1,12
- 2018 : 1,08
- 2019 : 0,79

La dispersion augmente ensuite entre 2020 et 2022, atteignant 2,91 en 2022, avant de diminuer de nouveau pour atteindre 0,83 en 2025.

La CEMAC présente une évolution beaucoup plus irrégulière. Son écart-type atteint notamment 5,78 en 2016, contre seulement 0,96 en 2021, avant de remonter à 3,73 en 2025.

### Interprétation

Les performances de croissance des pays de l'UEMOA apparaissent globalement plus homogènes que celles des pays de la CEMAC.

L'UEMOA connaît toutefois une période d'augmentation de la dispersion entre 2020 et 2022, suivie d'une diminution marquée entre 2023 et 2025.

À l'inverse, la CEMAC présente des variations importantes de dispersion selon les années. Cette évolution traduit une plus grande hétérogénéité des performances nationales et une sensibilité plus importante aux trajectoires individuelles de certains pays.

L'écart-type utilisé ici mesure la dispersion des taux de croissance entre les pays pour une année donnée. Il ne doit pas être confondu avec la dispersion des niveaux de PIB réel par habitant, qui sera examinée dans l'analyse de la σ-convergence.

## 5. Comparaison de la dispersion moyenne sur la période 2015-2025

### Objectif

Comparer le niveau moyen de dispersion annuelle des taux de croissance entre l'UEMOA et la CEMAC sur l'ensemble de la période.

### Requête SQL utilisée

```sql
WITH dispersion_annuelle AS (
    SELECT
        i.annee,
        p.zone,
        STDDEV_POP(i.croissance_pib) AS ecart_type
    FROM indicateurs_economiques i
    JOIN pays p
        ON i.id_pays = p.id_pays
    GROUP BY
        i.annee,
        p.zone
)

SELECT
    zone,
    ROUND(AVG(ecart_type), 2) AS dispersion_moyenne
FROM dispersion_annuelle
GROUP BY zone
ORDER BY dispersion_moyenne;
```

### Résultats

- UEMOA : **1,45 point**
- CEMAC : **3,31 points**

### Interprétation

Entre 2015 et 2025, les taux de croissance des pays de l'UEMOA ont été en moyenne nettement moins dispersés que ceux des pays de la CEMAC.

L'écart-type annuel moyen s'établit à 1,45 point pour l'UEMOA, contre 3,31 points pour la CEMAC. Ce résultat confirme une plus grande homogénéité des rythmes de croissance au sein de l'UEMOA.

La CEMAC présente au contraire des écarts de performance plus importants entre ses États membres.

Il s'agit ici d'une comparaison de la dispersion des taux de croissance, calculée à partir de la moyenne des écarts-types annuels. Ce résultat ne permet pas, à lui seul, de conclure à une convergence ou à une divergence des niveaux de revenu.

## 6. Conclusion de l'analyse des dynamiques de croissance

L'analyse de la période 2015-2025 met en évidence deux différences majeures entre les zones étudiées.

Premièrement, l'UEMOA enregistre une croissance moyenne du PIB réel nettement supérieure à celle de la CEMAC, avec 5,27 % contre 0,86 % sur la période.

Deuxièmement, les performances des pays de l'UEMOA sont globalement plus homogènes. La dispersion annuelle moyenne des taux de croissance s'établit à 1,45 point en UEMOA, contre 3,31 points en CEMAC.

Ces résultats indiquent donc que l'UEMOA combine, sur la période étudiée, une croissance plus élevée et une plus grande homogénéité des performances nationales de croissance.

Cependant, cette première analyse porte uniquement sur les taux de croissance du PIB réel. Elle permet d'évaluer les différences de performance et d'homogénéité des rythmes de croissance, mais ne suffit pas à établir l'existence d'une convergence économique des niveaux de revenu.

L'analyse est donc complétée par l'étude de la σ-convergence et de la β-convergence à partir du PIB réel par habitant.

## 7. Analyse de la convergence économique

### 7.1. σ-convergence

La σ-convergence mesure l'évolution de la dispersion des niveaux de PIB réel par habitant entre les pays d'une même zone.

La mesure utilisée est l'écart-type de la distribution des logarithmes du PIB réel par habitant :

```sql
STDDEV_POP(LN(pib_reel_par_habitant))
```

Une diminution de cet indicateur signifie que les écarts relatifs entre les niveaux de PIB réel par habitant se réduisent. À l'inverse, une augmentation traduit un élargissement de la dispersion.

#### CEMAC

Entre 2015 et 2025, la valeur de σ diminue de **1,1100 à 0,9488**, soit une baisse d'environ 14,5 %.

Cette évolution descriptive est compatible avec une tendance à la σ-convergence. Toutefois, elle doit être interprétée avec prudence.

L'analyse de sensibilité montre que le retrait de la Guinée équatoriale réduit d'environ 68 % la diminution de la dispersion. La baisse observée dépend donc fortement de la présence de ce pays.

Par ailleurs, l'intervalle de confiance bootstrap à 95 % de la variation de σ entre 2015 et 2025 est compris entre **-0,324 et +0,029**. Comme cet intervalle inclut zéro, les données ne permettent pas de confirmer statistiquement une diminution de la dispersion dans cet exercice.

Il est donc plus rigoureux de parler d'une baisse descriptive de la dispersion, compatible avec une tendance à la σ-convergence, plutôt que d'une σ-convergence établie.

#### UEMOA

Sur la même période, σ augmente légèrement de **0,3892 à 0,4234**, soit une hausse d'environ 8,8 %.

Cette évolution indique un élargissement modéré de la dispersion des niveaux de PIB réel par habitant.

L'intervalle de confiance bootstrap à 95 % de la variation est compris entre **+0,002 et +0,055**. Il est entièrement positif dans cette estimation, ce qui va dans le sens d'une légère hausse de la dispersion. Toutefois, le nombre limité de pays invite à éviter toute interprétation excessive de ce résultat.

L'UEMOA reste néanmoins beaucoup plus homogène que la CEMAC en matière de niveaux de PIB réel par habitant sur la période étudiée.

#### Synthèse de la σ-convergence

Les deux zones présentent des évolutions descriptives opposées :

- **CEMAC :** diminution de la dispersion des niveaux de PIB réel par habitant entre 2015 et 2025.
- **UEMOA :** légère augmentation de cette dispersion sur la même période.

Ces résultats décrivent une évolution de l'hétérogénéité des revenus, mais ne permettent pas à eux seuls de déterminer si les pays les moins riches connaissent un véritable rattrapage économique.

La sensibilité des résultats aux pays individuels, particulièrement en CEMAC, doit également être prise en compte.

### 7.2. β-convergence

La β-convergence cherche à déterminer si les pays ayant un niveau initial de PIB réel par habitant plus faible ont tendance à enregistrer une croissance plus rapide que les pays initialement plus riches.

L'analyse repose ici sur une régression de **β-convergence absolue**, réalisée séparément pour les deux zones, sans variable explicative supplémentaire.

Les variables étudiées sont les suivantes :

- **X :** logarithme du PIB réel par habitant en 2015.
- **Y :** croissance annuelle moyenne du logarithme du PIB réel par habitant entre 2015 et 2025.

La variable dépendante est calculée selon la formule :

```text
Y = 100 × (LN(PIB réel par habitant en 2025)
           - LN(PIB réel par habitant en 2015)) / 10
```

La division par 10 correspond aux dix intervalles annuels entre 2015 et 2025. Il s'agit d'un taux de croissance logarithmique annualisé, et non d'une moyenne arithmétique des taux de croissance annuels.

Une pente négative est compatible avec une relation de β-convergence : les pays initialement moins riches enregistreraient une croissance moyenne plus élevée. Une pente positive va dans le sens opposé.

Toutefois, le signe du coefficient ne suffit pas à établir l'existence d'une relation statistiquement significative. La valeur p, l'intervalle de confiance et la sensibilité de l'estimation doivent également être examinés.

#### CEMAC

La régression donne les résultats suivants :

| Indicateur | Résultat |
|---|---:|
| Coefficient β | -1,646 |
| Erreur standard | 0,905 |
| Statistique t | -1,819 |
| Valeur p | 0,143 |
| R² | 0,453 |
| Intervalle de confiance à 95 % | [-4,158 ; +0,866] |
| Nombre de pays | 6 |

La pente négative indique que les pays ayant un niveau initial de PIB réel par habitant plus élevé ont eu tendance à enregistrer une croissance moyenne plus faible.

Ce résultat va dans le sens d'une possible β-convergence. Cependant, la valeur p de 0,143 est supérieure au seuil de 5 % et l'intervalle de confiance inclut zéro.

Les vérifications complémentaires ne modifient pas cette conclusion : le test avec erreurs standards robustes HC3 donne p = 0,285, le test exact de permutation p = 0,150 et la corrélation de rang de Spearman p = 0,111.

La relation observée n'est donc pas statistiquement significative selon les méthodes examinées. Les données ne permettent pas de confirmer une β-convergence au sein de la CEMAC.

Les analyses de sensibilité montrent également que le résultat dépend de certains pays. Le retrait du Gabon modifie sensiblement l'estimation : le coefficient passe à -2,512 et devient statistiquement significatif au seuil de 5 % (p = 0,029). À l'inverse, le retrait de la Guinée équatoriale réduit la valeur absolue du coefficient à -0,651 et conduit à une valeur p de 0,507.

Ces variations montrent que l'estimation est sensible à la composition du groupe de pays étudié. Elles renforcent la nécessité d'interpréter le coefficient initial avec prudence.

#### UEMOA

La régression donne les résultats suivants :

| Indicateur | Résultat |
|---|---:|
| Coefficient β | +0,771 |
| Erreur standard | 0,622 |
| Statistique t | 1,239 |
| Valeur p | 0,262 |
| R² | 0,204 |
| Intervalle de confiance à 95 % | [-0,751 ; +2,293] |
| Nombre de pays | 8 |

La pente positive indique que les pays ayant un niveau initial de PIB réel par habitant plus élevé ont eu tendance à enregistrer une croissance moyenne légèrement supérieure.

Toutefois, cette relation n'est pas statistiquement significative selon la régression classique (p = 0,262) et l'intervalle de confiance inclut zéro.

Les tests de permutation et de corrélation de Spearman ne mettent pas non plus en évidence de relation statistiquement significative : leurs valeurs p sont respectivement de 0,266 et 0,120.

Le test avec erreurs standards robustes HC3 donne toutefois une valeur p de 0,024. Ce résultat diffère des autres méthodes utilisées. Compte tenu du faible nombre de pays et de cette divergence entre les tests, il ne constitue pas une preuve suffisante pour conclure à une relation statistiquement établie.

Le coefficient ne permet donc pas de conclure à une β-convergence, mais il ne permet pas non plus d'établir une divergence statistiquement significative.

Le R² de 0,204 indique que le niveau initial de PIB réel par habitant explique une part limitée de la variation de la croissance moyenne entre les pays de l'UEMOA.

Les analyses de sensibilité montrent que le signe positif du coefficient est conservé lorsqu'un pays est retiré à la fois. Aucun pays ne présente toutefois une influence suffisamment forte pour modifier substantiellement l'interprétation générale de la régression.

#### Synthèse de la β-convergence

Les deux régressions présentent des coefficients de signes différents :

- **CEMAC :** coefficient négatif de -1,646, mais non significatif selon la régression classique (p = 0,143).
- **UEMOA :** coefficient positif de +0,771, mais non significatif selon la régression classique (p = 0,262).

Les résultats ne permettent donc pas de confirmer statistiquement une β-convergence dans l'une ou l'autre des deux zones.

En CEMAC, la pente négative constitue un indice descriptif compatible avec un possible rattrapage, mais sa sensibilité à certains pays et son absence de significativité empêchent d'en faire une conclusion établie.

En UEMOA, la pente positive ne permet pas davantage de démontrer une divergence des revenus. Le résultat HC3 significatif, contrairement aux autres tests, doit être considéré comme une analyse de sensibilité et non comme une conclusion définitive.

### 7.3. Synthèse de l'analyse de convergence

Les analyses de σ-convergence et de β-convergence mettent en évidence des évolutions différentes entre les deux zones.

- **CEMAC :** la dispersion des niveaux de PIB réel par habitant diminue entre 2015 et 2025 et le coefficient de β-convergence est négatif. Toutefois, la baisse de dispersion reste sensible à la présence de la Guinée équatoriale et la régression ne présente pas de relation statistiquement significative selon les principaux tests examinés.
- **UEMOA :** la dispersion des niveaux de PIB réel par habitant augmente légèrement et le coefficient de β-convergence est positif. Cette relation n'est pas statistiquement significative selon la régression classique et les tests complémentaires, malgré un résultat HC3 différent.

Une zone peut donc présenter des niveaux de revenu relativement homogènes sans que ses pays soient engagés dans un processus de rattrapage. De même, une baisse de dispersion ne signifie pas nécessairement que les économies les moins riches progressent plus rapidement.

La convergence doit ainsi être étudiée à travers plusieurs indicateurs complémentaires, en tenant compte de la significativité statistique et de la sensibilité des résultats.

## 8. Synthèse générale de l'analyse exploratoire

L'analyse de la croissance et de la convergence économique met en évidence des différences importantes entre l'UEMOA et la CEMAC.

L'UEMOA se distingue par une croissance moyenne plus élevée et des taux de croissance nationaux globalement moins dispersés. Elle présente également des niveaux de PIB réel par habitant plus homogènes sur la période étudiée.

La CEMAC présente des performances de croissance plus contrastées, mais une diminution descriptive de la dispersion des niveaux de PIB réel par habitant entre 2015 et 2025. Cette baisse reste toutefois sensible à la présence de certains pays, notamment la Guinée équatoriale.

Les régressions de β-convergence ne permettent pas de confirmer statistiquement un processus de rattrapage dans l'une ou l'autre des deux zones. Les résultats doivent donc être interprétés comme des éléments d'analyse exploratoire et non comme la démonstration d'un mécanisme de convergence établi.

Ces observations montrent que la performance économique, l'homogénéité des rythmes de croissance et la convergence des niveaux de revenu sont trois dimensions distinctes. Leur analyse conjointe permet d'obtenir une lecture plus nuancée des trajectoires économiques des deux unions monétaires.

Les principaux résultats relatifs à la croissance sont présentés dans le tableau de bord interactif réalisé avec Power BI. Les analyses détaillées de σ-convergence et de β-convergence sont documentées dans cette analyse exploratoire et dans les fichiers de travail associés.

