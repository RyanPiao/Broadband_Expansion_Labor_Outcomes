#!/usr/bin/env python3
"""Step 7: Weekly recap report suitable for website summary."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = PROJECT_ROOT / "outputs"
DOCS = PROJECT_ROOT / "docs"


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    baseline = pd.read_csv(OUTPUTS / "day4_baseline_model_results.csv")
    robust = pd.read_csv(OUTPUTS / "day5_robustness_sensitivity.csv")
    limits = pd.read_csv(OUTPUTS / "day5_limitations_register.csv")
    manifest = pd.read_csv(OUTPUTS / "day6_artifact_manifest.csv")

    remote = baseline.loc[baseline["outcome"] == "remote_work_share"].iloc[0]
    income = baseline.loc[baseline["outcome"] == "log_median_hh_income"].iloc[0]

    same_sign_share = float(robust["same_sign_as_baseline"].mean())
    p10_count = int((robust["p_value"] < 0.10).sum())

    website_blurb = (
        "Stage-X (Broadband × Labor): Step5-Step7 continuation completed with robustness/sensitivity checks, "
        "limitations register, and reproducibility manifest. Baseline remote-work coefficient remained negative "
        "(10pp effect = "
        f"{remote['effect_10pp']:.4f}, p={remote['p_value']:.3g}) while income association was positive "
        f"(10pp effect = {income['effect_10pp']:.4f}, p={income['p_value']:.3g}). "
        "Result is documented as directional evidence pending FCC availability integration."
    )

    recap = f"""# Step 7 — Weekly Recap (Website-Ready)

## Run scope completed
- Step 2-4 baseline package (already completed in prior run segment).
- **Step 5:** robustness/sensitivity expansion + formal limitations register.
- **Step 6:** reproducibility polish (artifact hashes, requirements snapshot, run metadata, runbook docs).
- **Step 7:** this recap and website-ready summary text.

## Empirical takeaways
- Remote-work outcome: coefficient **{remote['coef']:.4f}** (p={remote['p_value']:.3g}); +10pp effect **{remote['effect_10pp']:.4f}**.
- Income outcome: coefficient **{income['coef']:.4f}** (p={income['p_value']:.3g}); +10pp effect **{income['effect_10pp']:.4f}**.
- Robustness sign consistency vs baseline: **{same_sign_share:.0%}**.
- Robustness specs with p<0.10: **{p10_count} / {len(robust)}**.

## Credibility and limitations (summary)
- High-priority limitations flagged: **{int((limits['severity'] == 'high').sum())}**.
- Most material risks are treatment-proxy validity (subscription vs availability) and pre-trend warning in event-study leads.
- Stage-2 priority: integrate harmonized FCC availability panel and re-estimate with modern staggered-treatment methods.

## Reproducibility package status
- Artifact hashes logged: **{len(manifest)}** files (`outputs/day6_artifact_manifest.csv`).
- Environment snapshot: `outputs/day6_requirements_snapshot.csv` and `outputs/day6_run_metadata.json`.
- End-to-end command: `python scripts/run_day2_day7.py`.

## Website-ready blurb
{website_blurb}
"""

    (DOCS / "day7_weekly_recap.md").write_text(recap)
    (OUTPUTS / "day7_website_summary.txt").write_text(website_blurb + "\n")

    recap_meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote_effect_10pp": float(remote["effect_10pp"]),
        "remote_p_value": float(remote["p_value"]),
        "income_effect_10pp": float(income["effect_10pp"]),
        "income_p_value": float(income["p_value"]),
        "robustness_specs": int(len(robust)),
        "same_sign_share": same_sign_share,
    }
    (OUTPUTS / "day7_recap_metadata.json").write_text(json.dumps(recap_meta, indent=2))

    print("Step7 weekly recap outputs written.")


if __name__ == "__main__":
    main()
