"""Reproduit les analyses statistiques avancées du projet UEMOA / CEMAC.

Le script lit les tables propres du dépôt et écrit les résultats CSV dans
07_Resultats_Analyses/. Les calculs sont descriptifs ou exploratoires; ils ne
permettent pas d'inférer un effet causal de l'appartenance à une union.
"""

from __future__ import annotations

from itertools import combinations, permutations
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats


RACINE = Path(__file__).resolve().parents[1]
DOSSIER_DONNEES = RACINE / "02_Donnees_Nettoyees"
DOSSIER_RESULTATS = RACINE / "07_Resultats_Analyses"
ANNEES = tuple(range(2015, 2026))
GRAINE_ALEATOIRE = 20261105
N_BOOTSTRAP = 20_000


def charger_donnees() -> pd.DataFrame:
    """Lit et contrôle le panel pays-année utilisé dans les analyses."""
    pays = pd.read_csv(
        DOSSIER_DONNEES / "dim_pays.csv",
        encoding="utf-8-sig",
        dtype={"id_pays": "int64"},
    )
    indicateurs = pd.read_csv(
        DOSSIER_DONNEES / "fact_indicateurs.csv",
        encoding="utf-8-sig",
        dtype={"id_pays": "int64", "annee": "int64"},
    )

    colonnes_pays = {"id_pays", "nom_pays", "zone"}
    colonnes_indicateurs = {
        "id_pays",
        "annee",
        "croissance_pib",
        "pib_reel_par_habitant",
    }
    if not colonnes_pays.issubset(pays.columns):
        raise ValueError(f"Colonnes manquantes dans dim_pays.csv : {colonnes_pays - set(pays.columns)}")
    if not colonnes_indicateurs.issubset(indicateurs.columns):
        raise ValueError(
            "Colonnes manquantes dans fact_indicateurs.csv : "
            f"{colonnes_indicateurs - set(indicateurs.columns)}"
        )
    if pays["id_pays"].duplicated().any():
        raise ValueError("dim_pays.csv contient plusieurs lignes pour un même id_pays.")
    if indicateurs.duplicated(["id_pays", "annee"]).any():
        raise ValueError("fact_indicateurs.csv contient un doublon pays-année.")

    panel = indicateurs.merge(
        pays[["id_pays", "nom_pays", "zone"]],
        on="id_pays",
        how="left",
        validate="many_to_one",
    )
    if panel["nom_pays"].isna().any():
        raise ValueError("Certains id_pays de fact_indicateurs.csv ne sont pas décrits dans dim_pays.csv.")
    if panel[["croissance_pib", "pib_reel_par_habitant"]].isna().any().any():
        raise ValueError("Les indicateurs contiennent des valeurs manquantes.")
    if (panel["pib_reel_par_habitant"] <= 0).any():
        raise ValueError("Le PIB réel par habitant doit être positif pour calculer son logarithme.")

    annees = tuple(sorted(panel["annee"].unique()))
    if annees != ANNEES:
        raise ValueError(f"Période inattendue : {annees}; période attendue : {ANNEES}.")
    if panel["id_pays"].nunique() != 14 or len(panel) != 154:
        raise ValueError("Le panel attendu contient 14 pays et 154 observations pays-année.")
    observations_par_pays = panel.groupby("id_pays")["annee"].nunique()
    if not observations_par_pays.eq(len(ANNEES)).all():
        raise ValueError("Le panel doit contenir les onze années pour chacun des pays.")
    if set(panel["zone"].unique()) != {"UEMOA", "CEMAC"}:
        raise ValueError("Les deux zones attendues sont UEMOA et CEMAC.")

    panel["log_pib_reel_par_habitant"] = np.log(panel["pib_reel_par_habitant"])
    return panel.sort_values(["zone", "id_pays", "annee"]).reset_index(drop=True)


def enregistrer(table: pd.DataFrame, nom_fichier: str) -> None:
    DOSSIER_RESULTATS.mkdir(parents=True, exist_ok=True)
    table.to_csv(DOSSIER_RESULTATS / nom_fichier, index=False, encoding="utf-8-sig")


def calculer_croissance(panel: pd.DataFrame) -> None:
    """Compare les moyennes par pays et les moyennes annuelles ajustées par année."""
    moyennes_pays = (
        panel.groupby(["zone", "id_pays", "nom_pays"], as_index=False)["croissance_pib"]
        .mean()
    )
    uemoa = moyennes_pays.loc[moyennes_pays["zone"] == "UEMOA", "croissance_pib"].to_numpy()
    cemac = moyennes_pays.loc[moyennes_pays["zone"] == "CEMAC", "croissance_pib"].to_numpy()
    difference = float(uemoa.mean() - cemac.mean())

    test_welch = stats.ttest_ind(uemoa, cemac, equal_var=False)
    variance_uemoa = uemoa.var(ddof=1)
    variance_cemac = cemac.var(ddof=1)
    terme_uemoa = variance_uemoa / len(uemoa)
    terme_cemac = variance_cemac / len(cemac)
    erreur_type = np.sqrt(terme_uemoa + terme_cemac)
    degres_liberte = (terme_uemoa + terme_cemac) ** 2 / (
        terme_uemoa**2 / (len(uemoa) - 1) + terme_cemac**2 / (len(cemac) - 1)
    )
    marge = stats.t.ppf(0.975, degres_liberte) * erreur_type

    toutes_moyennes = moyennes_pays["croissance_pib"].to_numpy()
    n_uemoa = len(uemoa)
    statistiques_permutation = []
    for indices_uemoa in combinations(range(len(toutes_moyennes)), n_uemoa):
        masque = np.zeros(len(toutes_moyennes), dtype=bool)
        masque[list(indices_uemoa)] = True
        statistiques_permutation.append(
            toutes_moyennes[masque].mean() - toutes_moyennes[~masque].mean()
        )
    p_permutation = np.mean(
        np.abs(statistiques_permutation) >= abs(difference) - 1e-12
    )
    test_mann_whitney = stats.mannwhitneyu(
        uemoa,
        cemac,
        alternative="two-sided",
        method="exact",
    )

    panel_avec_zone = panel.assign(indicatrice_uemoa=(panel["zone"] == "UEMOA").astype(int))
    modele_panel = smf.ols(
        "croissance_pib ~ indicatrice_uemoa + C(annee)",
        data=panel_avec_zone,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": panel_avec_zone["id_pays"]},
    )
    intervalle_panel = modele_panel.conf_int().loc["indicatrice_uemoa"]

    lignes = [
        {
            "methode": "Welch sur les moyennes nationales",
            "estimation_uemoa_moins_cemac": difference,
            "p_value": float(test_welch.pvalue),
            "ic95_bas": float(difference - marge),
            "ic95_haut": float(difference + marge),
            "n_uemoa": len(uemoa),
            "n_cemac": len(cemac),
            "note": "Une observation par pays; moyennes calculées sur 2015-2025.",
        },
        {
            "methode": "Permutation exacte des moyennes nationales",
            "estimation_uemoa_moins_cemac": difference,
            "p_value": float(p_permutation),
            "ic95_bas": np.nan,
            "ic95_haut": np.nan,
            "n_uemoa": len(uemoa),
            "n_cemac": len(cemac),
            "note": "Test bilatéral sur les 3003 répartitions possibles de 8 pays parmi 14.",
        },
        {
            "methode": "Mann-Whitney exact sur les moyennes nationales",
            "estimation_uemoa_moins_cemac": difference,
            "p_value": float(test_mann_whitney.pvalue),
            "ic95_bas": np.nan,
            "ic95_haut": np.nan,
            "n_uemoa": len(uemoa),
            "n_cemac": len(cemac),
            "note": "Comparaison de rangs; test bilatéral exact.",
        },
        {
            "methode": "OLS avec effets fixes année et erreurs regroupées par pays",
            "estimation_uemoa_moins_cemac": float(modele_panel.params["indicatrice_uemoa"]),
            "p_value": float(modele_panel.pvalues["indicatrice_uemoa"]),
            "ic95_bas": float(intervalle_panel.iloc[0]),
            "ic95_haut": float(intervalle_panel.iloc[1]),
            "n_uemoa": len(uemoa),
            "n_cemac": len(cemac),
            "note": "154 lignes; erreurs standards regroupées sur 14 pays.",
        },
    ]
    enregistrer(pd.DataFrame(lignes), "tests_croissance.csv")


def construire_donnees_beta(panel: pd.DataFrame) -> pd.DataFrame:
    """Calcule le niveau initial et la croissance annualisée par pays."""
    debut_fin = panel.loc[panel["annee"].isin([2015, 2025])].pivot(
        index=["id_pays", "nom_pays", "zone"],
        columns="annee",
        values="log_pib_reel_par_habitant",
    )
    debut_fin = debut_fin.reset_index()
    debut_fin["log_pib_initial"] = debut_fin[2015]
    debut_fin["croissance_annuelle_pct"] = (debut_fin[2025] - debut_fin[2015]) / 10 * 100
    return debut_fin.sort_values(["zone", "log_pib_initial"]).reset_index(drop=True)


def pente_ols(x: np.ndarray, y: np.ndarray) -> float:
    x_centree = x - x.mean()
    y_centree = y - y.mean()
    return float(np.dot(x_centree, y_centree) / np.dot(x_centree, x_centree))


def analyser_beta(panel: pd.DataFrame) -> None:
    points = construire_donnees_beta(panel)
    enregistrer(
        points[["zone", "nom_pays", "log_pib_initial", "croissance_annuelle_pct"]]
        .assign(
            log_pib_initial=lambda table: table["log_pib_initial"].round(4),
            croissance_annuelle_pct=lambda table: table["croissance_annuelle_pct"].round(2),
        ),
        "beta_convergence_uemoa_cemac.csv",
    )

    lignes_regression = []
    lignes_sensibilite = []
    for zone in ("CEMAC", "UEMOA"):
        donnees_zone = points.loc[points["zone"] == zone].copy()
        x = donnees_zone["log_pib_initial"].to_numpy(dtype=float)
        y = donnees_zone["croissance_annuelle_pct"].to_numpy(dtype=float)
        modele = sm.OLS(y, sm.add_constant(x)).fit()
        robuste = modele.get_robustcov_results(cov_type="HC3")
        correlation = stats.spearmanr(x, y)

        pente_observee = pente_ols(x, y)
        pentes_permutes = (
            pente_ols(x, np.asarray(y_permutee))
            for y_permutee in permutations(y)
        )
        p_permutation = np.mean(
            [abs(pente) >= abs(pente_observee) - 1e-12 for pente in pentes_permutes]
        )

        lignes_regression.extend(
            [
                {
                    "zone": zone,
                    "methode": "OLS classique",
                    "coefficient_beta": pente_observee,
                    "r_carre": float(modele.rsquared),
                    "p_value": float(modele.pvalues[1]),
                    "ic95_bas": float(modele.conf_int()[1, 0]),
                    "ic95_haut": float(modele.conf_int()[1, 1]),
                    "n_pays": len(donnees_zone),
                },
                {
                    "zone": zone,
                    "methode": "OLS, erreurs standards HC3",
                    "coefficient_beta": pente_observee,
                    "r_carre": float(modele.rsquared),
                    "p_value": float(robuste.pvalues[1]),
                    "ic95_bas": float(robuste.conf_int()[1, 0]),
                    "ic95_haut": float(robuste.conf_int()[1, 1]),
                    "n_pays": len(donnees_zone),
                },
                {
                    "zone": zone,
                    "methode": "Corrélation de Spearman",
                    "coefficient_beta": float(correlation.statistic),
                    "r_carre": np.nan,
                    "p_value": float(correlation.pvalue),
                    "ic95_bas": np.nan,
                    "ic95_haut": np.nan,
                    "n_pays": len(donnees_zone),
                },
                {
                    "zone": zone,
                    "methode": "Permutation exacte de la pente",
                    "coefficient_beta": pente_observee,
                    "r_carre": float(modele.rsquared),
                    "p_value": float(p_permutation),
                    "ic95_bas": np.nan,
                    "ic95_haut": np.nan,
                    "n_pays": len(donnees_zone),
                },
            ]
        )

        for index, ligne in donnees_zone.iterrows():
            sans_un_pays = donnees_zone.drop(index)
            lignes_sensibilite.append(
                {
                    "zone": zone,
                    "pays_retiré": ligne["nom_pays"],
                    "coefficient_beta_restant": pente_ols(
                        sans_un_pays["log_pib_initial"].to_numpy(dtype=float),
                        sans_un_pays["croissance_annuelle_pct"].to_numpy(dtype=float),
                    ),
                    "n_pays_restants": len(sans_un_pays),
                }
            )

    enregistrer(pd.DataFrame(lignes_regression), "beta_regressions.csv")
    enregistrer(pd.DataFrame(lignes_sensibilite), "beta_sensibilite.csv")


def analyser_sigma(panel: pd.DataFrame) -> None:
    par_annee = (
        panel.groupby(["annee", "zone"], as_index=False)["log_pib_reel_par_habitant"]
        .agg(sigma=lambda valeurs: valeurs.std(ddof=0))
        .sort_values(["annee", "zone"])
    )
    enregistrer(
        par_annee.assign(sigma=lambda table: table["sigma"].round(4)),
        "sigma_convergence_uemoa_cemac.csv",
    )

    generateur = np.random.default_rng(GRAINE_ALEATOIRE)
    lignes = []
    for zone in ("CEMAC", "UEMOA"):
        donnees_zone = panel.loc[panel["zone"] == zone]
        trajectoires = donnees_zone.loc[
            donnees_zone["annee"].isin([2015, 2025])
        ].pivot(index="id_pays", columns="annee", values="log_pib_reel_par_habitant")
        valeurs_2015 = trajectoires[2015].to_numpy(dtype=float)
        valeurs_2025 = trajectoires[2025].to_numpy(dtype=float)
        difference_sigma = float(
            np.std(valeurs_2025, ddof=0) - np.std(valeurs_2015, ddof=0)
        )

        indices = generateur.integers(
            0,
            len(trajectoires),
            size=(N_BOOTSTRAP, len(trajectoires)),
        )
        differences_reechantillonnees = (
            np.std(valeurs_2025[indices], axis=1, ddof=0)
            - np.std(valeurs_2015[indices], axis=1, ddof=0)
        )
        borne_basse, borne_haute = np.quantile(
            differences_reechantillonnees,
            [0.025, 0.975],
        )

        nom_exclu = "Guinée équatoriale" if zone == "CEMAC" else None
        trajectoires_sans = trajectoires.copy()
        if nom_exclu:
            id_exclu = donnees_zone.loc[
                donnees_zone["nom_pays"] == nom_exclu, "id_pays"
            ].unique()
            trajectoires_sans = trajectoires_sans.drop(index=id_exclu, errors="ignore")
            values_sans_2015 = trajectoires_sans[2015].to_numpy(dtype=float)
            values_sans_2025 = trajectoires_sans[2025].to_numpy(dtype=float)
            difference_sans = float(
                np.std(values_sans_2025, ddof=0) - np.std(values_sans_2015, ddof=0)
            )
            part_reduction = (
                1 - abs(difference_sans) / abs(difference_sigma)
                if difference_sigma != 0
                else np.nan
            )
        else:
            difference_sans = np.nan
            part_reduction = np.nan

        lignes.append(
            {
                "zone": zone,
                "delta_sigma_2025_moins_2015": difference_sigma,
                "bootstrap_ic95_bas": float(borne_basse),
                "bootstrap_ic95_haut": float(borne_haute),
                "graine": GRAINE_ALEATOIRE,
                "repetitions_bootstrap": N_BOOTSTRAP,
                "pays_exclu_pour_sensibilite": nom_exclu or "",
                "delta_sigma_sans_pays": difference_sans,
                "part_de_la_baisse_reduite": part_reduction,
                "note": "Bootstrap apparié par pays sur les valeurs 2015 et 2025.",
            }
        )

    enregistrer(pd.DataFrame(lignes), "sigma_sensibilite.csv")


def main() -> None:
    panel = charger_donnees()
    calculer_croissance(panel)
    analyser_beta(panel)
    analyser_sigma(panel)
    print("Analyses terminées. Les fichiers CSV sont disponibles dans 07_Resultats_Analyses/.")


if __name__ == "__main__":
    main()
