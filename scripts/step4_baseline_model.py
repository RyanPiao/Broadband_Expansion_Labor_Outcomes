#!/usr/bin/env python3
"""Step 4: Baseline model estimation + diagnostics (efficient TWFE implementation)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ANALYSIS = PROJECT_ROOT / "data_analysis"
OUTPUTS = PROJECT_ROOT / "outputs"

EVENT_WINDOW = [-3, -2, 0, 1, 2, 3]  # omitted baseline is -1
ADOPTION_THRESHOLD = 0.70


def twfe_transform(df: pd.DataFrame, cols: List[str], entity: str = "county_id", time: str = "year") -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        ent_mean = out.groupby(entity)[c].transform("mean")
        time_mean = out.groupby(time)[c].transform("mean")
        overall = out[c].mean()
        out[f"{c}_twfe"] = out[c] - ent_mean - time_mean + overall
    return out


def fit_twfe(df: pd.DataFrame, outcome: str, regressors: List[str]) -> Dict[str, float]:
    needed = [outcome, *regressors]
    d = df.dropna(subset=needed).copy()
    d = twfe_transform(d, needed)

    y = d[f"{outcome}_twfe"]
    X = d[[f"{r}_twfe" for r in regressors]]

    model = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": d["state_fips"]})

    key = f"broadband_sub_share_twfe"
    coef = float(model.params.get(key, np.nan))
    se = float(model.bse.get(key, np.nan))
    p = float(model.pvalues.get(key, np.nan))

    return {
        "outcome": outcome,
        "coef": coef,
        "se": se,
        "p_value": p,
        "effect_10pp": 0.10 * coef,
        "n_obs": int(model.nobs),
        "r2": float(model.rsquared),
    }


def build_event_sample(df: pd.DataFrame, threshold: float = ADOPTION_THRESHOLD) -> pd.DataFrame:
    d = df.sort_values(["county_id", "year"]).copy()

    adoption_year = (
        d.loc[d["broadband_sub_share"] >= threshold]
        .groupby("county_id")["year"]
        .min()
        .rename("adoption_year")
    )
    d = d.merge(adoption_year, on="county_id", how="left")
    d["event_time"] = d["year"] - d["adoption_year"]
    d["ever_treated"] = d["adoption_year"].notna().astype(int)

    for k in EVENT_WINDOW:
        key = f"event_m{abs(k)}" if k < 0 else f"event_{k}"
        d[key] = (d["event_time"] == k).astype(int)

    return d


def run_event_study(df: pd.DataFrame) -> pd.DataFrame:
    terms = [f"event_m{abs(k)}" if k < 0 else f"event_{k}" for k in EVENT_WINDOW]
    regressors = [*terms, "unemployment_rate", "log_population"]

    d = df.dropna(subset=["remote_work_share", *regressors]).copy()
    d = twfe_transform(d, ["remote_work_share", *regressors])

    y = d["remote_work_share_twfe"]
    X = d[[f"{r}_twfe" for r in regressors]]
    model = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": d["state_fips"]})

    rows = []
    for k in EVENT_WINDOW:
        key = f"event_m{abs(k)}" if k < 0 else f"event_{k}"
        twfe_key = f"{key}_twfe"
        coef = float(model.params.get(twfe_key, np.nan))
        se = float(model.bse.get(twfe_key, np.nan))
        p = float(model.pvalues.get(twfe_key, np.nan))
        rows.append(
            {
                "event_time": k,
                "coef": coef,
                "se": se,
                "p_value": p,
                "ci_low": coef - 1.96 * se,
                "ci_high": coef + 1.96 * se,
            }
        )

    return pd.DataFrame(rows)


def diagnostics(es_df: pd.DataFrame, es: pd.DataFrame, baseline_remote: Dict[str, float]) -> pd.DataFrame:
    pre = es[es["event_time"].isin([-3, -2])]
    pretrend_pass = bool((pre["p_value"] > 0.10).all())

    county_adopt = es_df.groupby("county_id")["adoption_year"].first()
    ever_treated_share = float(county_adopt.notna().mean())
    n_treated_cohorts = int(county_adopt.dropna().nunique())

    support_pass = bool((ever_treated_share >= 0.20) and (n_treated_cohorts >= 3))
    sign_pass = bool(baseline_remote["coef"] > 0)

    rows = [
        {
            "diagnostic": "pretrend_gate_p_gt_0.10_for_k_-3_-2",
            "value": float(pretrend_pass),
            "rule": "both pre-period p-values > 0.10",
            "pass": int(pretrend_pass),
        },
        {
            "diagnostic": "treatment_support_ever_treated_share",
            "value": ever_treated_share,
            "rule": ">=0.20",
            "pass": int(ever_treated_share >= 0.20),
        },
        {
            "diagnostic": "treatment_support_n_treated_cohorts",
            "value": float(n_treated_cohorts),
            "rule": ">=3",
            "pass": int(n_treated_cohorts >= 3),
        },
        {
            "diagnostic": "combined_support_gate",
            "value": float(support_pass),
            "rule": "share and cohorts thresholds both pass",
            "pass": int(support_pass),
        },
        {
            "diagnostic": "primary_sign_gate_remote_work",
            "value": float(sign_pass),
            "rule": "remote-work coefficient > 0",
            "pass": int(sign_pass),
        },
    ]
    return pd.DataFrame(rows)


def plot_event(es: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(es["event_time"], es["coef"], yerr=1.96 * es["se"], fmt="o-", capsize=4)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(-0.5, color="gray", linestyle="--", linewidth=1)
    ax.set_title("Step4 Event Study: Remote Work vs Broadband Adoption")
    ax.set_xlabel("Event time (baseline = -1 omitted)")
    ax.set_ylabel("Coefficient")
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_ANALYSIS / "county_year_panel.csv")
    df = df.copy()
    df["log_population"] = np.where(df["population"] > 0, np.log(df["population"]), np.nan)

    model_df = df.dropna(
        subset=[
            "remote_work_share",
            "digital_emp_share",
            "log_median_hh_income",
            "broadband_sub_share",
            "unemployment_rate",
            "log_population",
        ]
    ).copy()

    regressors = ["broadband_sub_share", "unemployment_rate", "log_population"]

    baseline_rows = [
        fit_twfe(model_df, "remote_work_share", regressors),
        fit_twfe(model_df, "digital_emp_share", regressors),
        fit_twfe(model_df, "log_median_hh_income", regressors),
    ]
    baseline = pd.DataFrame(baseline_rows)
    baseline.to_csv(OUTPUTS / "day4_baseline_model_results.csv", index=False)

    es_df = build_event_sample(model_df)
    es = run_event_study(es_df)
    es.to_csv(OUTPUTS / "day4_event_study_results.csv", index=False)
    plot_event(es, OUTPUTS / "day4_event_study_plot.png")

    diag = diagnostics(es_df, es, baseline_rows[0])
    diag.to_csv(OUTPUTS / "day4_model_diagnostics.csv", index=False)

    support = (
        es_df.groupby("year", as_index=False)
        .agg(
            counties=("county_id", "nunique"),
            mean_treatment=("broadband_sub_share", "mean"),
            ever_treated_share=("ever_treated", "mean"),
        )
    )
    support.to_csv(OUTPUTS / "day4_model_sample_support.csv", index=False)

    print("Step4 baseline model outputs written.")


if __name__ == "__main__":
    main()
