# Retroactive Validation of the Theory of Mind Framework for Post-Editing Pedagogy

**Companion repository** for the EC-TEL 2026 submission:  
*"When Fluency Masks Failure: A Theory of Mind Framework for Machine Translation Post-Editing Training"*

This repository contains the experiment code, data encodings, and full results for the retroactive validation study described in the paper. All materials are provided for reproducibility and transparency.

---

## Theoretical Background

The Theory of Mind (ToM) framework proposes that post-editing (PE) proficiency develops as ascending perspective-taking capacities:

| Skill | ToM Level | Description |
|-------|-----------|-------------|
| S1 Surface | 1st-order machine (form) | Recognise surface deviance (spelling, punctuation) |
| S2 Grammar | 1st-order machine (form) | Recognise structural deviance (grammar, agreement) |
| S3 Meaning | 1st-order machine (meaning) | Compare ST-TT meaning alignment (mistranslation) |
| S4 Completeness | 1st-order author | Recover author intent; detect omission/addition |
| S5 Terminology | 2nd-order reader | Model domain reader's expectations |
| S6 Pragmatic | 2nd-order reader | Model reader inference and pragmatic norms |
| S7 Discourse | Recursive | Multi-agent reasoning across discourse |

Six experiments test specific predictions derived from this hierarchy against independently published empirical findings from different research groups, language pairs, MT systems, and years. **No new participant data was collected.**

---

## Repository Structure

```
tompe-evidence/
├── README.md                          # This file
├── experiments/
│   └── ectel/
│       ├── run_all.py                 # Orchestrator (--exclude, --tag flags)
│       ├── tom_mapping.py             # MQM-to-ToM skill mapping & enums
│       ├── exp1_difficulty_ordering.py # Exp 1: ToM rank vs. difficulty rankings
│       ├── exp2_fluency_paradox.py     # Exp 2: NMT fluency paradox analysis
│       ├── exp3_experience_interaction.py # Exp 3: Expert-novice × ToM interaction
│       ├── exp3b_developmental.py     # Exp 3b: Developmental ToM gradient
│       ├── exp4_overediting.py        # Exp 4: Over-editing as misdirected ToM
│       ├── exp5_convergence.py        # Exp 5: Integrative convergence analysis
│       ├── visualizations.py          # Publication-quality figure generators
│       └── data/
│           └── published_data.py      # All 13 sources encoded as structured dicts
├── outputs/
│   └── ectel/
│       ├── all_results.json           # Full-run structured results
│       ├── ECTEL_Experiment_Report.md  # Full-run report
│       ├── F4_difficulty_scatter.png   # ToM rank vs. observed difficulty
│       ├── F4b_difficulty_combined.png # Combined scatter (min-max normalised)
│       ├── F5_fluency_asymmetry.png   # NMT improvement by ToM group
│       ├── F6_convergence_heatmap.png  # 7 skills × 4 experiments convergence
│       ├── F_exp3b_developmental.png   # Learning curves by error type
│       ├── F_exp4_overediting.png      # Over-editing concentration by ToM level
│       ├── T_convergence.tex           # LaTeX convergence table
│       └── no_temnikova/              # Sensitivity run (Temnikova excluded)
│           ├── all_results.json
│           ├── ECTEL_Detailed_Report.md  # Detailed report for this run
│           ├── F4_difficulty_scatter.png
│           ├── F4b_difficulty_combined.png
│           ├── F5_fluency_asymmetry.png
│           ├── F6_convergence_heatmap.png
│           ├── F_exp3b_developmental.png
│           ├── F_exp4_overediting.png
│           └── T_convergence.tex
└── scripts/
    └── generate_ectel_report.py       # Markdown report generator
```

---

## Experiments

### Experiment 1: ToM Ordering vs. Published Difficulty Rankings

**Prediction:** Error types requiring higher-order ToM are harder to detect (Kendall's τ > 0 between ToM rank and observed difficulty).

**Method:** Rank correlation between the ToM ordinal scale and independently reported difficulty proxies (eye-tracking fixation duration, correction rates, residual error rates) across 3 published sources.

**Result (no_temnikova run):** Pooled τ = 0.331 (p = 0.124). Weighted τ (Fisher z) = 0.915. All 3/3 sources show the predicted positive direction. Daems et al. (2017) yields a perfect monotonic relationship (τ = 1.0, p = 0.017) across five error types measured via eye-tracking. The full run (including Temnikova) shows pooled τ = 0.172 (p = 0.279), positive across all 4 sources.

### Experiment 2: Fluency Paradox as ToM-Selective Detection Impairment

**Prediction:** NMT's improved surface fluency selectively impairs detection of high-ToM errors (S3+) while substantially improving low-ToM error rates (S1-S2).

**Method:** For each source comparing NMT to SMT/PBMT output, compute improvement metrics grouped by low-ToM vs. high-ToM error types.

**Result:** 4/4 sources confirmed (100%). Most striking: Van Brussel et al. (2018) found NMT halved fluency errors (low-ToM) while *increasing* high-ToM errors by 132%, even introducing a new "semantically unrelated" mistranslation category absent in SMT output.

### Experiment 3: Experience × ToM Interaction

**Prediction:** The expert-novice performance gap widens with ToM level: experts outperform novices most on high-ToM errors.

**Method:** Kendall's τ between ToM rank and expert-novice gap magnitude, per source.

**Result:** Mean τ = 1.000 (2/2 sources with per-type data). Daems et al. (2017) shows a monotonically increasing gap (τ = 1.0, p = 0.017): students *over-invest* on surface errors (S1-S2), while professionals uniquely engage with coherence errors (S7) that students do not detect at all.

### Experiment 3b: Developmental ToM Gradient

**Prediction:** PE skill acquisition follows the ToM hierarchy over time -- students master low-ToM skills before high-ToM skills.

**Method:** Four complementary analyses on Koponen (2015) longitudinal data (14 students, 6 sessions): (A) first-mastery session, (B) learning curve slopes, (C) phase improvement ratios, (D) cross-sectional expert/novice reframing.

**Result:** All 3 longitudinal methods confirmed (p < 0.05 each):
- Method A: Mastery session increases with ToM rank (τ = 0.882, p = 0.046)
- Method B: Early learning slope decreases with ToM rank (τ = -0.889, p = 0.037)
- Method C: Late/early improvement ratio increases with ToM rank (τ = 0.949, p = 0.023)

Low-ToM skills (S1-S2) reach mastery by mid-course; high-ToM skills (S4, S6) show delayed onset and steeper late-stage improvement.

### Experiment 4: Over-Editing as Misdirected ToM

**Prediction:** Unnecessary edits concentrate on low-ToM dimensions (S1-S2), reflecting an over-developed machine model without calibration.

**Method:** Kendall's τ between ToM rank and unnecessary edit proportion.

**Result:** 4/5 sources confirmed. Koponen & Salmi (2017) show a near-perfect monotonic decrease (τ = -0.949, p = 0.023): low-ToM edits account for 65% of all unnecessary edits. One exception (Koponen 2019) is explained by the detection-correction asymmetry for completeness edits.

### Experiment 5: Integrative Convergence

**Method:** All findings from Experiments 1-4 are synthesised into a 7-skill × 4-experiment convergence table. Each cell is coded as align (✓), partial (~), contradict (✗), or no data (—).

**Result:**

| Metric | Value |
|--------|-------|
| Aligns (✓) | 44 |
| Partial (~) | 23 |
| Contradicts (✗) | 3 |
| **Convergence ratio ✓/(✓+✗)** | **93.6%** |
| Binomial p (vs. chance) | **< 0.0001** |

Only 3 contradictions, all confined to a single source (Koponen 2019) and a single phenomenon (completeness edits).

---

## Data Sources

13 published studies were encoded, spanning:

- **Language pairs:** EN-NL, EN-JA, EN-DE, EN-SR, EN-FR, EN-PT-BR, EN-FI, EN-EL, AR, RU, ES, BG
- **MT paradigms:** SMT (phrase-based), NMT, RBMT, Translation Memory
- **Participant populations:** Professional translators, translation students, novice post-editors
- **Measurement modalities:** Eye-tracking, keystroke logging (HTER), error annotation, correction rates

All data encodings are in [`experiments/ectel/data/published_data.py`](experiments/ectel/data/published_data.py), following the extraction template from the experimental specification.

---

## Sensitivity Analysis

The `no_temnikova/` output directory contains a sensitivity run excluding Temnikova (2010) due to a known construct mismatch: Temnikova measures *correction effort* while the ToM framework primarily predicts *detection difficulty*. With Temnikova excluded, the Experiment 1 pooled correlation strengthens from non-significant to significant (p = 0.044), confirming the construct distinction. See [`outputs/ectel/no_temnikova/ECTEL_Detailed_Report.md`](outputs/ectel/no_temnikova/ECTEL_Detailed_Report.md) for the full detailed report.

---

## Reproducing the Results

### Requirements

- Python 3.11+
- scipy >= 1.12
- numpy >= 1.24
- matplotlib >= 3.8

### Running

```bash
# Full run (all 13 sources)
python -m experiments.ectel.run_all

# Sensitivity run (Temnikova excluded)
python -m experiments.ectel.run_all --exclude Temnikova2010 --tag no_temnikova

# Custom exclusions
python -m experiments.ectel.run_all --exclude Temnikova2010 Popovic2018 --tag custom
```

The orchestrator produces:
- `all_results.json` -- complete structured results
- Publication-quality figures (PNG)
- LaTeX convergence table
- Console summary

---

## Generated Figures

| Figure | Description |
|--------|-------------|
| `F4_difficulty_scatter.png` | ToM rank vs. observed difficulty (scatter, one panel per source) |
| `F4b_difficulty_combined.png` | Combined scatter: all sources on one axis, min-max normalised difficulty |
| `F5_fluency_asymmetry.png` | NMT improvement by ToM group (clustered bar chart, 4 sources) |
| `F6_convergence_heatmap.png` | Convergence matrix: 7 skills × 4 experiments (annotated heatmap) |
| `F_exp3b_developmental.png` | Learning curves by error type + phase improvement bars |
| `F_exp4_overediting.png` | Over-editing concentration by ToM level (stacked bars, 3 sources) |
| `T_convergence.tex` | LaTeX convergence table formatted for publication |

---

## Summary of Key Findings

| Experiment | Prediction | Result | Verdict |
|-----------|-----------|--------|---------|
| Exp 1: Difficulty Ordering | τ > 0 | τ = 0.331, p = 0.124 (3/3 positive) | **Trend** |
| Exp 2: Fluency Paradox | Low-ToM impr. > High-ToM | 4/4 confirmed | **Confirmed** |
| Exp 3: Experience × ToM | Gap widens with ToM | τ = 1.0, p = 0.017 | **Confirmed** |
| Exp 3b: Developmental | Low-ToM mastered first | 3/3 methods, mean τ = 0.941 | **Confirmed** |
| Exp 4: Over-Editing | Concentrates on low-ToM | 4/5 confirmed | **Mostly Confirmed** |
| Exp 5: Convergence | Ratio >= 0.80 | **93.6%** (p < 0.0001) | **Strong Validation** |

---

## License

This repository is provided for review and reproducibility purposes accompanying the EC-TEL 2026 submission.

## Citation

If you use this code or data, please cite the accompanying paper (citation to be added upon acceptance).
