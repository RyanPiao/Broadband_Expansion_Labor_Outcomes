# DAY1_problem_framing.md

## Day 1 Problem Framing (Week-1 Build, Fresh Start)

### 1) Framing summary
I am initiating a new empirical tech-economics workflow on the labor-market consequences of broadband infrastructure expansion. Day 1 is dedicated to locking the research design before estimation.

**Selected topic (senior-level empirical/quant):**  
**Broadband expansion and local labor-market adjustment in the remote-work era.**

---

### 2) Core research question
**What is the causal effect of increased county-level high-speed broadband availability on remote-work participation, digital-sector employment, and wages?**

This question is policy-relevant because broadband subsidies and infrastructure programs are often justified by productivity and labor-market inclusion claims, but causal evidence remains mixed across contexts.

---

### 3) Estimands (locked on Day 1)
Let treatment be county-year broadband coverage rate (>=100/20 Mbps availability).

1. **Primary estimand:**
   - Change in remote-work share associated with a 10 pp increase in coverage.
2. **Secondary estimand 1:**
   - Change in digital-intensive sector employment share.
3. **Secondary estimand 2:**
   - Change in county wage outcomes (log median wage / mean weekly wage).

Interpretation target: medium-run response (1-3 years after coverage expansion).

---

### 4) Data strategy (Public Real first)
**Data Type:** **Public Real Data (selected)**

Planned public sources:
- FCC broadband availability data (BDC and/or harmonized Form 477 history),
- ACS county outcomes and demographics,
- BLS QCEW/OEWS/LAUS labor outcomes,
- BEA regional controls.

**Feasibility judgment:** Public real data are sufficient to execute Day 1-Week 1 scope; synthetic fallback is not required at this stage.

---

### 5) Identification options (ranked)

#### Option A — Staggered DiD / event-study (primary)
Exploit variation in timing/intensity of broadband expansion across counties.
- Credibility checks: pre-trends, dynamic lead/lag profile, treatment-support diagnostics.

#### Option B — Shift-share predicted exposure (robustness)
Use pre-period telecom structure interacted with national rollout growth to reduce direct endogeneity.

#### Option C — Border-county comparison (supplement)
Compare adjacent counties across policy/program boundaries with different rollout intensity.

#### Option D — IV specification (conditional)
Use infrastructure-cost shifters only if first-stage strength and exclusion logic are defensible.

---

### 6) Core risks to causal interpretation
1. **Targeted rollout bias:** providers may expand where outcomes would improve anyway.
2. **Measurement discontinuity risk:** transition from Form 477 to BDC reporting regimes.
3. **Pandemic confounding:** remote work and broadband both shifted sharply around 2020.
4. **Policy overlap:** broadband grants may coincide with local workforce initiatives.
5. **Aggregate-data limits:** county-level estimates cannot identify individual household mechanisms.

Mitigation plan: explicit pre-trend diagnostics, alternative treatment definitions, time-window sensitivity, state-year policy controls, and restrained interpretation language.

---

### 7) Reproducibility plan (Day 1 commitments)
- Build a script-only pipeline (download, clean, merge, estimate, output).
- Version all assumptions and inclusion/exclusion rules in markdown.
- Save source metadata (URL, access date, schema notes).
- Keep generated outputs separate from raw pulls.
- Ensure baseline tables can be regenerated from a single run command after Day 2 extraction.

---

### 8) What is complete at end of Day 1
- Research question and estimands are explicitly defined.
- Public-real data path is selected and justified.
- Identification menu is prioritized with credibility checks.
- Key risks and interpretation boundaries are documented.
- Reproducibility expectations are locked before analysis.
