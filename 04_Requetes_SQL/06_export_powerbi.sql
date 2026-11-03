USE convergence_uemoa_cemac;


-- =====================================================
-- 1. DIMENSION PAYS
-- =====================================================

SELECT
    id_pays,
    nom_pays,
    code_pays,
    zone,
    monnaie
FROM pays
ORDER BY id_pays;


-- =====================================================
-- 2. TABLE DE FAITS : INDICATEURS ECONOMIQUES
-- =====================================================

SELECT
    id_pays,
    annee,
    croissance_pib,
    pib_reel_par_habitant
FROM indicateurs_economiques
ORDER BY
    id_pays,
    annee;