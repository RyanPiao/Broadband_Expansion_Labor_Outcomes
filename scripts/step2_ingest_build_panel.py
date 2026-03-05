#!/usr/bin/env python3
"""Step 2: Ingestion + specification lock support + QA for county-year panel.

Data source: Public real ACS 5-year API (2017-2023).
This script builds the analysis panel and enforces fail-stop QA checks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data_raw"
DATA_INTERMEDIATE = PROJECT_ROOT / "data_intermediate"
DATA_ANALYSIS = PROJECT_ROOT / "data_analysis"
OUTPUTS = PROJECT_ROOT / "outputs"

YEARS = list(range(2017, 2024))
BASE_URL = "https://api.census.gov/data/{year}/acs/acs5"

ACS_VARS: Dict[str, str] = {
    "B08006_001E": "workers_total",
    "B08006_017E": "workers_wfh",
    "B28002_001E": "hh_total",
    "B28002_004E": "hh_broadband",
    "B19013_001E": "median_hh_income",
    "B23025_003E": "labor_force",
    "B23025_005E": "unemployed",
    "B01003_001E": "population",
    "C24030_001E": "emp_total",
    "C24030_013E": "male_info",
    "C24030_040E": "female_info",
    "C24030_015E": "male_finance",
    "C24030_042E": "female_finance",
    "C24030_018E": "male_prof_sci",
    "C24030_045E": "female_prof_sci",
    "C24030_019E": "male_mgmt",
    "C24030_046E": "female_mgmt",
}

CORE_VARS = [
    "remote_work_share",
    "broadband_sub_share",
    "digital_emp_share",
    "log_median_hh_income",
    "unemployment_rate",
    "population",
]


@dataclass
class SourceRecord:
    year: int
    url: str
    access_utc: str
    rows: int


def fetch_year(year: int) -> pd.DataFrame:
    vars_list = ["NAME", *ACS_VARS.keys()]
    params = {"get": ",".join(vars_list), "for": "county:*"}
    url = BASE_URL.format(year=year)
    response = requests.get(url, params=params, timeout=90)
    response.raise_for_status()
    payload = response.json()

    header = payload[0]
    rows = payload[1:]
    df = pd.DataFrame(rows, columns=header)
    df["year"] = year

    df["state"] = pd.to_numeric(df["state"], errors="coerce")
    df = df[df["state"] <= 56].copy()

    for col in ACS_VARS.keys():
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def engineer_panel(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["state_fips"] = out["state"].astype(int).astype(str).str.zfill(2)
    out["county_fips"] = out["county"].astype(str).str.zfill(3)
    out["county_id"] = out["state_fips"] + out["county_fips"]

    out = out.rename(columns=ACS_VARS)

    def safe_div(numer: pd.Series, denom: pd.Series) -> pd.Series:
        denom_safe = denom.where(denom > 0)
        return numer / denom_safe

    out["remote_work_share"] = safe_div(out["workers_wfh"], out["workers_total"])
    out["broadband_sub_share"] = safe_div(out["hh_broadband"], out["hh_total"])

    out["digital_emp_count"] = (
        out["male_info"]
        + out["female_info"]
        + out["male_finance"]
        + out["female_finance"]
        + out["male_prof_sci"]
        + out["female_prof_sci"]
        + out["male_mgmt"]
        + out["female_mgmt"]
    )
    out["digital_emp_share"] = safe_div(out["digital_emp_count"], out["emp_total"])
    out["unemployment_rate"] = safe_div(out["unemployed"], out["labor_force"])

    out["log_median_hh_income"] = np.where(
        out["median_hh_income"] > 0,
        np.log(out["median_hh_income"]),
        np.nan,
    )

    # Pre-specified series-break indicator rule for when FCC harmonized data is added.
    # Kept in panel now for reproducibility consistency (0 in ACS-only fallback phase).
    out["fcc_series_break_post_2022"] = (out["year"] >= 2022).astype(int)

    share_cols = ["remote_work_share", "broadband_sub_share", "digital_emp_share", "unemployment_rate"]
    for col in share_cols:
        out.loc[(out[col] < 0) | (out[col] > 1), col] = np.nan

    keep_cols = [
        "year",
        "state_fips",
        "county_fips",
        "county_id",
        "NAME",
        "workers_total",
        "workers_wfh",
        "remote_work_share",
        "hh_total",
        "hh_broadband",
        "broadband_sub_share",
        "emp_total",
        "digital_emp_count",
        "digital_emp_share",
        "median_hh_income",
        "log_median_hh_income",
        "labor_force",
        "unemployed",
        "unemployment_rate",
        "population",
        "fcc_series_break_post_2022",
    ]
    out = out[keep_cols].sort_values(["county_id", "year"]).reset_index(drop=True)
    return out


def run_qa(panel: pd.DataFrame) -> pd.DataFrame:
    checks: List[dict] = []

    checks.append(
        {
            "check": "year_range_locked_2017_2023",
            "metric": int(set(panel["year"].unique()) == set(YEARS)),
            "threshold": 1,
            "pass": int(set(panel["year"].unique()) == set(YEARS)),
            "notes": "Panel year set must match lock exactly.",
        }
    )

    dup_count = int(panel.duplicated(["county_id", "year"]).sum())
    checks.append(
        {
            "check": "unique_county_year_key",
            "metric": dup_count,
            "threshold": 0,
            "pass": int(dup_count == 0),
            "notes": "No duplicate county_id-year rows allowed.",
        }
    )

    min_counties = int(panel.groupby("year")["county_id"].nunique().min())
    checks.append(
        {
            "check": "county_coverage_per_year",
            "metric": min_counties,
            "threshold": 3100,
            "pass": int(min_counties >= 3100),
            "notes": "Expected contiguous county coverage in ACS 5y extract.",
        }
    )

    for col in CORE_VARS:
        non_missing = float(panel[col].notna().mean())
        checks.append(
            {
                "check": f"non_missing_{col}",
                "metric": round(non_missing, 6),
                "threshold": 0.95,
                "pass": int(non_missing >= 0.95),
                "notes": "Core variable non-missing share threshold.",
            }
        )

    for col in ["remote_work_share", "broadband_sub_share", "digital_emp_share", "unemployment_rate"]:
        bounded = float(panel[col].dropna().between(0, 1, inclusive="both").mean())
        checks.append(
            {
                "check": f"bounded_{col}",
                "metric": round(bounded, 6),
                "threshold": 1.0,
                "pass": int(np.isclose(bounded, 1.0)),
                "notes": "All non-missing share values must be in [0,1].",
            }
        )

    full_panel_share = float(
        panel.groupby("county_id")["year"].nunique().eq(len(YEARS)).mean()
    )
    checks.append(
        {
            "check": "full_panel_share",
            "metric": round(full_panel_share, 6),
            "threshold": 0.9,
            "pass": int(full_panel_share >= 0.9),
            "notes": "Share of counties with complete year coverage.",
        }
    )

    qa = pd.DataFrame(checks)
    return qa


def write_outputs(raw: pd.DataFrame, panel: pd.DataFrame, manifest: List[SourceRecord], qa: pd.DataFrame) -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_INTERMEDIATE.mkdir(parents=True, exist_ok=True)
    DATA_ANALYSIS.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    raw_path = DATA_RAW / f"day2_acs_raw_{min(YEARS)}_{max(YEARS)}.csv"
    panel_path = DATA_INTERMEDIATE / "day2_county_year_panel.csv"
    analysis_path = DATA_ANALYSIS / "county_year_panel.csv"

    raw.to_csv(raw_path, index=False)
    panel.to_csv(panel_path, index=False)
    panel.to_csv(analysis_path, index=False)

    pd.DataFrame([m.__dict__ for m in manifest]).to_csv(OUTPUTS / "day2_source_manifest.csv", index=False)
    qa.to_csv(OUTPUTS / "day2_qa_report.csv", index=False)

    missingness = (
        panel.isna()
        .mean()
        .rename("missing_share")
        .reset_index()
        .rename(columns={"index": "variable"})
        .sort_values("missing_share", ascending=False)
    )
    missingness.to_csv(OUTPUTS / "day2_missingness_by_variable.csv", index=False)

    sample = (
        panel.groupby("year", as_index=False)
        .agg(
            county_count=("county_id", "nunique"),
            avg_remote_work=("remote_work_share", "mean"),
            avg_broadband=("broadband_sub_share", "mean"),
        )
    )
    sample.to_csv(OUTPUTS / "day2_sample_by_year.csv", index=False)

    summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "years": [min(YEARS), max(YEARS)],
        "rows": int(len(panel)),
        "counties": int(panel["county_id"].nunique()),
        "fail_stop_triggered": bool((qa["pass"] == 0).any()),
        "raw_path": str(raw_path.relative_to(PROJECT_ROOT)),
        "panel_path": str(panel_path.relative_to(PROJECT_ROOT)),
    }
    (OUTPUTS / "day2_panel_build_summary.json").write_text(json.dumps(summary, indent=2))


def main() -> None:
    frames = []
    manifest: List[SourceRecord] = []

    for year in YEARS:
        df_year = fetch_year(year)
        frames.append(df_year)
        manifest.append(
            SourceRecord(
                year=year,
                url=BASE_URL.format(year=year),
                access_utc=datetime.now(timezone.utc).isoformat(),
                rows=int(len(df_year)),
            )
        )

    raw = pd.concat(frames, ignore_index=True)
    panel = engineer_panel(raw)
    qa = run_qa(panel)
    write_outputs(raw, panel, manifest, qa)

    if (qa["pass"] == 0).any():
        failed = qa.loc[qa["pass"] == 0, "check"].tolist()
        raise RuntimeError(f"Step2 QA fail-stop triggered. Failed checks: {failed}")

    print("Step2 ingestion complete. QA checks passed.")


if __name__ == "__main__":
    main()
