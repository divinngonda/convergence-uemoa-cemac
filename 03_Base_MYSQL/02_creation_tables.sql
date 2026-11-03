USE convergence_uemoa_cemac;

CREATE TABLE pays (
    id_pays INT PRIMARY KEY,
    nom_pays VARCHAR(50) NOT NULL,
    code_pays VARCHAR(3) NOT NULL UNIQUE,
    zone VARCHAR(10) NOT NULL,
    monnaie VARCHAR(10) NOT NULL
);

CREATE TABLE indicateurs_economiques (
    id_indicateur INT NOT NULL AUTO_INCREMENT,
    id_pays INT NOT NULL,
    annee YEAR NOT NULL,
    croissance_pib DECIMAL(12,9),
    pib_reel_par_habitant DECIMAL(18,12),

    PRIMARY KEY (id_indicateur),

    UNIQUE (id_pays, annee),

    FOREIGN KEY (id_pays)
        REFERENCES pays(id_pays)
);