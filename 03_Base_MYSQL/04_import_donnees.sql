USE convergence_uemoa_cemac;

-- =====================================================
-- 1. IMPORT DES DONNEES DE CROISSANCE DU PIB
-- =====================================================

CREATE TABLE croissance_pib_import (
    country_name VARCHAR(100),
    country_code VARCHAR(3),
    annee INT,
    croissance_pib DECIMAL(12,9)
);

-- Le fichier CSV nettoyé est importé dans croissance_pib_import
-- via l'assistant Table Data Import Wizard de MySQL Workbench.

INSERT INTO indicateurs_economiques (
    id_pays,
    annee,
    croissance_pib
)
SELECT 
    p.id_pays,
    c.annee,
    c.croissance_pib
FROM croissance_pib_import c
JOIN pays p 
    ON c.country_code = p.code_pays;


-- =====================================================
-- 2. IMPORT DU PIB REEL PAR HABITANT
-- =====================================================

CREATE TABLE pib_reel_par_habitant_import (
    country_name VARCHAR(100),
    country_code VARCHAR(3),
    annee INT,
    pib_reel_par_habitant DECIMAL(18,12)
);

-- Le fichier CSV nettoyé est importé dans pib_reel_par_habitant_import
-- via l'assistant Table Data Import Wizard de MySQL Workbench.

UPDATE indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
JOIN pib_reel_par_habitant_import g
    ON g.country_code = p.code_pays
    AND g.annee = i.annee
SET i.pib_reel_par_habitant = g.pib_reel_par_habitant;


-- =====================================================
-- 3. CONTROLES DE QUALITE
-- =====================================================

-- Vérifier le nombre de lignes importées
SELECT COUNT(*) AS nb_lignes_croissance
FROM croissance_pib_import;

SELECT COUNT(*) AS nb_lignes_pib_habitant
FROM pib_reel_par_habitant_import;

SELECT COUNT(*) AS nb_lignes_table_principale
FROM indicateurs_economiques;


-- Vérifier les valeurs manquantes de PIB réel par habitant
SELECT COUNT(*) AS nb_valeurs_manquantes
FROM indicateurs_economiques
WHERE pib_reel_par_habitant IS NULL;


-- Vérifier visuellement quelques lignes
SELECT
    p.nom_pays,
    i.annee,
    i.croissance_pib,
    i.pib_reel_par_habitant
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
ORDER BY
    p.nom_pays,
    i.annee
LIMIT 20;

-- Vérifier l'absence de doublons pays-année
SELECT
    id_pays,
    annee,
    COUNT(*) AS nombre
FROM indicateurs_economiques
GROUP BY
    id_pays,
    annee
HAVING COUNT(*) > 1;


-- Vérifier que le PIB réel par habitant est strictement positif
-- nécessaire avant l'utilisation du logarithme LN()
SELECT
    p.nom_pays,
    i.annee,
    i.pib_reel_par_habitant
FROM indicateurs_economiques i
JOIN pays p
    ON i.id_pays = p.id_pays
WHERE i.pib_reel_par_habitant <= 0;








