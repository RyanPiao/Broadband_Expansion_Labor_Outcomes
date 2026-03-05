# PLAN.md

## Project
**Topic:** Broadband Infrastructure Expansion and Local Labor-Market Adjustment in the Remote-Work Era  
**Stage:** Stage 1 (Step 1 framing → Step 5 first empirical readout)  
**Data Priority:** **Public Real Data** (required and selected)

---

## 1) Stage Objective
Produce a credible first-pass causal estimate of how increases in high-speed broadband availability affect:
1. Remote-work participation,
2. Employment in digital-intensive sectors,
3. Wage outcomes at the county level.

By end of Stage 1, the project should deliver a transparent identification strategy, an analysis-ready panel, baseline estimates, and a limitations memo suitable for senior technical-economics review.

---

## 2) Core Research Question
**How does county-level expansion in high-speed fixed broadband coverage change remote-work labor outcomes and wage growth?**

Policy relevance: large public and private investments in broadband are often justified by productivity and inclusion claims; this project tests those claims empirically.

---

## 3) Main Estimands (pre-registered targets)
Let \(c\) index counties and \(t\) years.

1. **Primary estimand (ITT-style):**
   - Effect of a 10 percentage-point increase in broadband coverage (>=100/20 Mbps availability) on the county remote-work share.
2. **Secondary estimand A:**
   - Effect on employment share in digitally intensive industries (NAICS-based grouping).
3. **Secondary estimand B:**
   - Effect on median annual wage (or log weekly wage) at county level.

Interpretation target: medium-run (1-3 year) response, not immediate same-quarter effects.

---

## 4) Public Real Data Plan

### Core sources
- **FCC Broadband Data Collection (BDC)** or Form 477 historical series: county-level fixed broadband availability.
- **ACS 1-year / 5-year** (Census): remote-work share (work-from-home commute mode), demographic controls.
- **BLS QCEW/OEWS**: employment and wage outcomes by county/industry.
- **BEA Regional Data**: income and macro controls.
- **BLS LAUS**: unemployment and labor-force controls.

### Unit of analysis
County-year panel (with optional county-industry-year extension for sector heterogeneity).

### Public-data feasibility note
This topic is feasible with fully public datasets; **no synthetic fallback is currently required** for Step 1 framing.

---

## 5) Identification Strategy Menu

### Option A (Primary): Staggered DiD/event-study
Use differential timing/intensity of county broadband expansion.
- Model: two-way FE baseline + modern staggered-adoption estimators (e.g., Callaway-Sant'Anna / Sun-Abraham style implementation).
- Key checks: pre-trend tests, treatment timing support, dynamic effects.

### Option B: Shift-share exposure design
Construct predicted county exposure from pre-period telecom footprint × national rollout intensity.
- Use as robustness where rollout timing may be endogenous.

### Option C: Border-pair design (supplement)
Adjacent counties across state/program boundaries with differential rollout intensity.
- Focus on local comparability and reduced confounding.

### Option D: Instrumental variables (only if diagnostics pass)
Potential instrument class: engineering-cost shifters (terrain ruggedness / legacy infrastructure constraints) interacted with national deployment push.
- Use only with strong first stage and exclusion-logic defense.

---

## 6) Key Risks and Mitigations
1. **Endogenous rollout targeting** (providers expand where growth is already expected).  
   *Mitigation:* event-study diagnostics, richer county trends, shift-share robustness, border comparisons.

2. **Measurement change between Form 477 and BDC eras.**  
   *Mitigation:* harmonization protocol, series break indicators, restricted-window robustness.

3. **Pandemic-era confounding in remote work outcomes.**  
   *Mitigation:* flexible year effects, pandemic-period interactions, sensitivity excluding 2020 transition year.

4. **Ecological inference limits (county aggregates).**  
   *Mitigation:* explicit interpretation boundaries; avoid household-level causal language.

5. **Policy overlap (state grants, labor shocks).**  
   *Mitigation:* include state-year controls and policy indicator set where available.

---

## 7) Stage 1 Execution Schedule

### Step 1 (current)
- Lock problem framing, estimands, identification options, and risk register.
- Finalize public-data-first source map and reproducibility commitments.

### Step 2
- Build raw data ingestion scripts and codebook.
- Construct preliminary county-year panel and QA checks.

### Step 3
- Baseline descriptive diagnostics + first FE estimates.
- Produce event-study prototype and sample composition tables.

### Step 4
- Robustness pass: alternative treatment definitions, pre-trend windows, spillover checks.
- Heterogeneity cuts (rural/urban, low/high baseline coverage).

### Step 5
- Draft findings memo with credibility grading.
- Document unresolved identification threats and Stage 2 plan.

---

## 8) Reproducibility Plan
- Keep full pipeline script-based (no manual spreadsheet edits).
- Maintain clear folders: `data_raw/`, `data_intermediate/`, `data_analysis/`, `outputs/`, `scripts/`, `docs/`.
- Record exact source URLs, pull dates, and file hashes where possible.
- Pin package versions in `requirements.txt` / environment file.
- Add one-command rerun entry point after Step 2 extraction is stable.

---

## 9) Step 1 Deliverable Checklist
- [x] Senior-level empirical topic selected.
- [x] Public real data path prioritized and feasible.
- [x] Research question and estimands explicitly defined.
- [x] Identification options and risks documented.
- [x] Reproducibility commitments stated.
