#!/usr/bin/env python3
"""Day 3: Exploratory Data Analysis (EDA) outputs for county-year panel."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ANALYSIS = PROJECT_ROOT / "data_analysis"
OUTPUTS = PROJECT_ROOT / "outputs"


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_ANALYSIS / "county_year_panel.csv")

    key_vars = [
        "remote_work_share",
        "broadband_sub_share",
        "digital_emp_share",
        "median_hh_income",
        "unemployment_rate",
        "population",
    ]

    eda_df = df.copy()

    # 1) Summary statistics
    summary = eda_df[key_vars].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).T
    summary.to_csv(OUTPUTS / "day3_eda_summary_stats.csv")

    # 2) Missingness
    missing = (
        eda_df[key_vars]
        .isna()
        .mean()
        .rename("missing_share")
        .reset_index()
        .rename(columns={"index": "variable"})
        .sort_values("missing_share", ascending=False)
    )
    missing.to_csv(OUTPUTS / "day3_eda_missingness.csv", index=False)

    # 3) Yearly trends
    yearly = (
        eda_df.groupby("year", as_index=False)
        .agg(
            county_count=("county_id", "nunique"),
            remote_work_mean=("remote_work_share", "mean"),
            broadband_mean=("broadband_sub_share", "mean"),
            digital_emp_mean=("digital_emp_share", "mean"),
            unemployment_mean=("unemployment_rate", "mean"),
        )
    )
    yearly.to_csv(OUTPUTS / "day3_eda_yearly_means.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(yearly["year"], yearly["remote_work_mean"], marker="o", label="Remote work share")
    ax.plot(yearly["year"], yearly["broadband_mean"], marker="o", label="Broadband share")
    ax.plot(yearly["year"], yearly["digital_emp_mean"], marker="o", label="Digital employment share")
    ax.set_title("County-Year Means: Core Shares")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUTS / "day3_eda_trends.png", dpi=170)
    plt.close(fig)

    # 4) Distribution diagnostics
    fig, ax = plt.subplots(figsize=(8, 5))
    subset = eda_df[eda_df["year"].isin([2017, 2023])].copy()
    sns.kdeplot(data=subset, x="broadband_sub_share", hue="year", fill=True, common_norm=False, ax=ax)
    ax.set_title("Broadband Share Distribution: 2017 vs 2023")
    ax.set_xlabel("Broadband subscription share")
    fig.tight_layout()
    fig.savefig(OUTPUTS / "day3_eda_broadband_distribution.png", dpi=170)
    plt.close(fig)

    # 5) Correlations
    corr = eda_df[
        [
            "remote_work_share",
            "broadband_sub_share",
            "digital_emp_share",
            "unemployment_rate",
            "median_hh_income",
        ]
    ].corr()
    corr.to_csv(OUTPUTS / "day3_eda_correlation_matrix.csv")

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Matrix (EDA)")
    fig.tight_layout()
    fig.savefig(OUTPUTS / "day3_eda_correlation_heatmap.png", dpi=170)
    plt.close(fig)

    # 6) Support check for treatment variable
    support = (
        eda_df.groupby("year")["broadband_sub_share"]
        .agg(["min", "max", "mean", "std"]) 
        .reset_index()
    )
    support.to_csv(OUTPUTS / "day3_eda_treatment_support.csv", index=False)

    print("Day3 EDA outputs written.")


if __name__ == "__main__":
    main()
