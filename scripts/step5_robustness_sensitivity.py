#!/usr/bin/env python3
"""Step 5: Robustness/sensitivity package + limitations register."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List

import numpy as np
import pandas as pd
import statsmodels.api as sm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ANALYSIS = PROJECT_ROOT / "data_analysis"
OUTPUTS = PROJECT_ROOT / "outputs"
DOCS = PROJECT_ROOT / "docs"


def twfe_transform(df: pd.DataFrame, cols: List[str], entity: str = "county_id", time: str = "year") -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        ent_mean = out.groupby(entity)[c].transform("mean")
        time_mean = out.groupby(time)[c].transform("mean")
        overall = out[c].mean()
        out[f"{c}_twfe"] = out[c] - ent_mean - time_mean + overall
    return out


def fit_twfe(
    df: pd.DataFrame,
    outcome: str,
    treatment: str,
    controls: List[str],
    label: str,
    sample_note: str,
) -> Dict[str, float | str]:
    needed = [outcome, treatment, *controls]
    d = df.dropna(subset=needed).copy()
    if d.empty:
        return {
            "spec": label,
            "sample_note": sample_note,
            "coef": np.nan,
            "se": np.nan,
            "p_value": np.nan,
            "effect_10pp": np.nan,
            "n_obs": 0,
            "r2": np.nan,
        }

    d = twfe_transform(d, needed)
    y = d[f"{outcome}_twfe"]
    X = d[[f"{c}_twfe" for c in [treatment, *controls]]]

    model = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": d["state_fips"]})

    key = f"{treatment}_twfe"
    coef = float(model.params.get(key, np.nan))
    se = float(model.bse.get(key, np.nan))
    p_value = float(model.pvalues.get(key, np.nan))

    return {
        "spec": label,
        "sample_note": sample_note,
        "coef": coef,
        "se": se,
        "p_value": p_value,
        "effect_10pp": float(0.10 * coef),
        "n_obs": int(model.nobs),
        "r2": float(model.rsquared),
    }


def fit_first_difference(df: pd.DataFrame, outcome: str, treatment: str, controls: List[str]) -> Dict[str, float | str]:
    d = df.sort_values(["county_id", "year"]).copy()
    cols = [outcome, treatment, *controls]
    for col in cols:
        d[f"d_{col}"] = d.groupby("county_id")[col].diff()

    needed = [f"d_{outcome}", f"d_{treatment}", *[f"d_{c}" for c in controls]]
    d = d.dropna(subset=needed)

    if d.empty:
        return {
            "spec": "first_difference",
            "sample_note": "County first-difference sensitivity",
            "coef": np.nan,
            "se": np.nan,
            "p_value": np.nan,
            "effect_10pp": np.nan,
            "n_obs": 0,
            "r2": np.nan,
        }

    y = d[f"d_{outcome}"]
    X = d[[f"d_{treatment}", *[f"d_{c}" for c in controls]]]
    model = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": d["state_fips"]})

    coef = float(model.params.get(f"d_{treatment}", np.nan))
    se = float(model.bse.get(f"d_{treatment}", np.nan))
    p_value = float(model.pvalues.get(f"d_{treatment}", np.nan))

    return {
        "spec": "first_difference",
        "sample_note": "County first-difference sensitivity",
        "coef": coef,
        "se": se,
        "p_value": p_value,
        "effect_10pp": float(0.10 * coef),
        "n_obs": int(model.nobs),
        "r2": float(model.rsquared),
    }


def prepare_specs(df: pd.DataFrame) -> List[Dict[str, float | str]]:
    controls = ["unemployment_rate", "log_population"]

    full_panel_counties = (
        df.groupby("county_id")["year"].nunique().loc[lambda s: s == df["year"].nunique()].index
    )

    p1 = df["broadband_sub_share"].quantile(0.01)
    p99 = df["broadband_sub_share"].quantile(0.99)

    df_lag = df.sort_values(["county_id", "year"]).copy()
    df_lag["broadband_sub_share_l1"] = df_lag.groupby("county_id")["broadband_sub_share"].shift(1)

    df_lead = df.sort_values(["county_id", "year"]).copy()
    df_lead["broadband_sub_share_f1"] = df_lead.groupby("county_id")["broadband_sub_share"].shift(-1)

    specs: List[tuple[str, pd.DataFrame, str, str, List[str]]] = [
        (
            "baseline_replication",
            df,
            "broadband_sub_share",
            "Replicates Step4 baseline specification",
            controls,
        ),
        (
            "exclude_2020",
            df.loc[df["year"] != 2020].copy(),
            "broadband_sub_share",
            "Drops 2020 transition year",
            controls,
        ),
        (
            "full_panel_only",
            df.loc[df["county_id"].isin(full_panel_counties)].copy(),
            "broadband_sub_share",
            "Keeps counties observed in all years",
            controls,
        ),
        (
            "winsorized_treatment_1_99",
            df.assign(broadband_sub_share=df["broadband_sub_share"].clip(lower=p1, upper=p99)),
            "broadband_sub_share",
            "Winsorized treatment at 1st/99th percentiles",
            controls,
        ),
        (
            "lagged_treatment_l1",
            df_lag,
            "broadband_sub_share_l1",
            "Uses one-year lagged treatment",
            controls,
        ),
        (
            "placebo_future_treatment_f1",
            df_lead,
            "broadband_sub_share_f1",
            "Placebo with one-year lead treatment",
            controls,
        ),
        (
            "add_series_break_control",
            df,
            "broadband_sub_share",
            "Adds FCC post-2022 series-break control",
            [*controls, "fcc_series_break_post_2022"],
        ),
    ]

    rows = [
        fit_twfe(
            spec_df,
            outcome="remote_work_share",
            treatment=treat,
            controls=spec_controls,
            label=label,
            sample_note=note,
        )
        for (label, spec_df, treat, note, spec_controls) in specs
    ]

    rows.append(fit_first_difference(df, "remote_work_share", "broadband_sub_share", controls))

    return rows


def build_limitations(robust: pd.DataFrame, event: pd.DataFrame) -> pd.DataFrame:
    baseline_row = robust.loc[robust["spec"] == "baseline_replication"].iloc[0]
    pre = event.loc[event["event_time"].isin([-3, -2])].copy()
    pre_fail = bool((pre["p_value"] <= 0.10).any())

    limitations = [
        {
            "limitation": "Pre-trend warning in event-study leads",
            "severity": "high" if pre_fail else "medium",
            "evidence": f"Lead p-values: {', '.join(f'{x:.3f}' for x in pre['p_value'].tolist())}",
            "implication": "Potential violation of parallel trends; causal interpretation is weakened.",
            "week2_action": "Re-estimate with alternative estimators and narrower comparability windows.",
        },
        {
            "limitation": "Primary coefficient sign is negative for remote-work outcome",
            "severity": "high" if baseline_row["coef"] < 0 else "medium",
            "evidence": f"Baseline coef={baseline_row['coef']:.4f}, p={baseline_row['p_value']:.4g}",
            "implication": "Direction conflicts with the initial hypothesis; may reflect treatment proxy issues or confounding.",
            "week2_action": "Replace treatment proxy with FCC availability series and re-run design diagnostics.",
        },
        {
            "limitation": "ACS subscription proxy may not equal infrastructure availability",
            "severity": "high",
            "evidence": "Treatment uses household subscription share (B28002) rather than provider availability coverage.",
            "implication": "Adoption behavior and affordability may contaminate infrastructure effect estimates.",
            "week2_action": "Integrate harmonized FCC Form-477/BDC county availability measures.",
        },
        {
            "limitation": "County-level aggregates and ACS 5-year smoothing",
            "severity": "medium",
            "evidence": "Panel is county-year with rolling ACS 5-year estimates.",
            "implication": "Short-run changes and household-level mechanisms are not separately identified.",
            "week2_action": "Add alternative outcomes and sensitivity to excluding boundary years.",
        },
    ]
    return pd.DataFrame(limitations)


def write_day5_note(robust: pd.DataFrame, limits: pd.DataFrame) -> None:
    baseline = robust.loc[robust["spec"] == "baseline_replication"].iloc[0]
    sign_consistency = float((np.sign(robust["coef"].dropna()) == np.sign(baseline["coef"])).mean())
    significant = int((robust["p_value"] < 0.10).sum())

    top_table = robust[["spec", "coef", "p_value", "effect_10pp", "n_obs"]].copy()
    top_table["coef"] = top_table["coef"].map(lambda x: f"{x:.4f}" if pd.notna(x) else "nan")
    top_table["p_value"] = top_table["p_value"].map(lambda x: f"{x:.4g}" if pd.notna(x) else "nan")
    top_table["effect_10pp"] = top_table["effect_10pp"].map(lambda x: f"{x:.4f}" if pd.notna(x) else "nan")

    limitations_md = "\n".join(
        [
            f"- **{row.limitation}** ({row.severity}): {row.evidence}"
            for row in limits.itertuples(index=False)
        ]
    )

    note = f"""# Step 5 — Robustness/Sensitivity + Limitations

## Robustness and sensitivity summary
- Specifications run: **{len(robust)}**
- Specs with same sign as baseline: **{sign_consistency:.0%}**
- Specs with p-value < 0.10: **{significant} / {len(robust)}**
- Baseline effect (+10pp broadband on remote-work share): **{baseline['effect_10pp']:.4f}**

## Spec table (remote-work outcome)

| spec | coef | p_value | effect_10pp | n_obs |
|---|---:|---:|---:|---:|
{chr(10).join([f"| {r['spec']} | {r['coef']} | {r['p_value']} | {r['effect_10pp']} | {int(r['n_obs'])} |" for _, r in top_table.iterrows()])}

## Limitations register (Stage-1)
{limitations_md}

## Stage-2 implications
1. Prioritize treatment-measure upgrade (FCC availability harmonization).
2. Re-run with modern staggered-adoption estimators and stronger comparability restrictions.
3. Treat this stage's remote-work estimates as directional diagnostics, not final causal claims.
"""

    (DOCS / "day5_robustness_limitations.md").write_text(note)


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_ANALYSIS / "county_year_panel.csv")
    df["log_population"] = np.where(df["population"] > 0, np.log(df["population"]), np.nan)

    robust = pd.DataFrame(prepare_specs(df))
    baseline_coef = robust.loc[robust["spec"] == "baseline_replication", "coef"].iloc[0]
    robust["same_sign_as_baseline"] = (np.sign(robust["coef"]) == np.sign(baseline_coef)).astype(int)
    robust.to_csv(OUTPUTS / "day5_robustness_sensitivity.csv", index=False)

    event = pd.read_csv(OUTPUTS / "day4_event_study_results.csv")
    limitations = build_limitations(robust, event)
    limitations.to_csv(OUTPUTS / "day5_limitations_register.csv", index=False)

    write_day5_note(robust, limitations)
    print("Step5 robustness/sensitivity outputs written.")


if __name__ == "__main__":
    main()
