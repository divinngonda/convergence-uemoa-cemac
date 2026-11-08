USE convergence_uemoa_cemac;

-- Tables temporaires de réception des deux CSV préparés.
-- Exécuter ce script avant l'import manuel avec MySQL Workbench.

CREATE TABLE IF NOT EXISTS croissance_pib_import (
    country_name VARCHAR(100),
    country_code VARCHAR(3),
    annee INT,
    croissance_pib DECIMAL(12,9)
);

CREATE TABLE IF NOT EXISTS pib_reel_par_habitant_import (
    country_name VARCHAR(100),
    country_code VARCHAR(3),
    annee INT,
    pib_reel_par_habitant DECIMAL(18,12)
);
