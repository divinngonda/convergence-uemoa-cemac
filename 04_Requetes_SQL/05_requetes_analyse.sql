USE convergence_uemoa_cemac;


-- =====================================================
-- 1. CROISSANCE MOYENNE PAR ZONE
-- =====================================================

SELECT
    p.zone,
    ROUND(AVG(i.croissance_pib), 2) AS croissance_moyenne
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
GROUP BY
    p.zone
ORDER BY
    croissance_moyenne DESC;


-- =====================================================
-- 2. CROISSANCE MOYENNE PAR PAYS
-- =====================================================

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


-- =====================================================
-- 3. EVOLUTION ANNUELLE DE LA CROISSANCE PAR ZONE
-- =====================================================

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


-- =====================================================
-- 4. DISPERSION ANNUELLE DES TAUX DE CROISSANCE
-- =====================================================

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


-- =====================================================
-- 5. DISPERSION MOYENNE DES TAUX DE CROISSANCE
-- =====================================================

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
GROUP BY
    zone
ORDER BY
    dispersion_moyenne;


-- =====================================================
-- 6. SIGMA-CONVERGENCE
-- Dispersion du log du PIB reel par habitant
-- =====================================================

SELECT
    i.annee,
    p.zone,
    ROUND(
        STDDEV_POP(LN(i.pib_reel_par_habitant)),
        4
    ) AS sigma
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
GROUP BY
    i.annee,
    p.zone
ORDER BY
    i.annee,
    p.zone;


-- =====================================================
-- 7. PREPARATION DES DONNEES POUR LA BETA-CONVERGENCE
-- =====================================================

WITH pib_initial_final AS (
    SELECT
        p.zone,
        p.nom_pays,

        MAX(
            CASE
                WHEN i.annee = 2015
                THEN i.pib_reel_par_habitant
            END
        ) AS pib_hab_2015,

        MAX(
            CASE
                WHEN i.annee = 2025
                THEN i.pib_reel_par_habitant
            END
        ) AS pib_hab_2025

    FROM indicateurs_economiques i
    JOIN pays p
        ON i.id_pays = p.id_pays

    GROUP BY
        p.zone,
        p.nom_pays
)

SELECT
    zone,
    nom_pays,

    ROUND(
        LN(pib_hab_2015),
        4
    ) AS log_pib_initial,

    ROUND(
        (
            LN(pib_hab_2025)
            - LN(pib_hab_2015)
        ) / 10 * 100,
        2
    ) AS croissance_annuelle_pct

FROM pib_initial_final

ORDER BY
    zone,
    log_pib_initial;


-- =====================================================
-- 8. CALCUL DU COEFFICIENT BETA PAR ZONE
-- =====================================================

WITH pib_initial_final AS (
    SELECT
        p.zone,
        p.nom_pays,

        MAX(
            CASE
                WHEN i.annee = 2015
                THEN i.pib_reel_par_habitant
            END
        ) AS pib_hab_2015,

        MAX(
            CASE
                WHEN i.annee = 2025
                THEN i.pib_reel_par_habitant
            END
        ) AS pib_hab_2025

    FROM indicateurs_economiques i
    JOIN pays p
        ON i.id_pays = p.id_pays

    GROUP BY
        p.zone,
        p.nom_pays
),

donnees_beta AS (
    SELECT
        zone,
        nom_pays,
        LN(pib_hab_2015) AS x,

        (
            LN(pib_hab_2025)
            - LN(pib_hab_2015)
        ) / 10 * 100 AS y

    FROM pib_initial_final
)

SELECT
    zone,

    (
        COUNT(*) * SUM(x * y)
        - SUM(x) * SUM(y)
    )
    /
    (
        COUNT(*) * SUM(x * x)
        - SUM(x) * SUM(x)
    ) AS beta

FROM donnees_beta

GROUP BY
    zone;