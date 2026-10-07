# ToM-PE Evidence

Analysis code, data provenance and results behind the Theory of Mind (ToM) framework
of the [ToM-PE](https://github.com/diana-nurbakova/tompe) post-editing training
platform.

> Diana Nurbakova and Liana Ermakova. 2026. *When Fluency Masks Failure: A Theory of
> Mind Model of Error Detection in Machine Translation Post-Editing.* In Proceedings of
> the IEEE/WIC International Conference on Web Intelligence and Intelligent Agent
> Technology (WI-IAT 2026).

The repository holds two independent lines of evidence:

| Analysis | Question | Data | Code | Results |
|---|---|---|---|---|
| **ToM hierarchy validation** | Are errors at higher ToM levels detected by fewer expert raters? | WMT 2020 MQM, EN→DE, 3 raters per segment (public) | [experiments/tom_validation/](experiments/tom_validation/) | [EXPERIMENTS.md](outputs/tom_validation/EXPERIMENTS.md) |
| **Retroactive validation** | Are findings already published in post-editing research consistent with the framework? | Values extracted from published studies | [experiments/retroactive_validation/](experiments/retroactive_validation/) | [Experiment_Report.md](outputs/retroactive_validation/Experiment_Report.md) |

No ToM-PE participant data is used in either analysis.

---

## 1. ToM hierarchy validation (WMT 2020 MQM)

Errors are assigned to four **ToM levels** (L0 target-only pattern matching, L1
source consultation, L2 source-author model, L3 reader-facing impact). Detection
agreement among the three expert raters serves as a behavioural difficulty measure.

Headline results (from [EXPERIMENTS.md §16](outputs/tom_validation/EXPERIMENTS.md)):

- **H1:** detection rate decreases monotonically with ToM level (Jonckheere–Terpstra,
  τ-b = −0.141, p < 1e-6).
- **H2:** the effect holds after adjusting for severity, segment length and system
  quality, with crossed random effects of system and document (CLMM β = −0.326,
  95 % CI [−0.346, −0.307]).
- **H3:** raters differ in their sensitivity to ToM level (GLMM random-slope
  LR χ²(2) = 202.5, p < 1e-6).
- **Robustness:** significant in all 8 sensitivity variants. The direction is stable
  across IoU thresholds 0.3–0.7 but the effect size is not (τ-b −0.119 to −0.146),
  so claims should rest on the ordering rather than the magnitude.

This is the only analysis that tests the difficulty ordering quantitatively.

## 2. Retroactive validation (published studies)

Tests predictions of the seven-**skill** model (S1–S7) against findings reported in
published post-editing studies. The skills and the L0–L3 levels above are different
constructs used for different purposes, so their mappings are not expected to align.

Current status of the experiments can be found in
[Experiment_Report.md](outputs/retroactive_validation/Experiment_Report.md). The
repository keeps the original analysis numbering; the paper renumbers the two it
reports:

| Repository key | Paper | Status |
|---|---|---|
| `analysis1` | withdrawn (not testable on this literature) | Still run for audit, not counted: no verified source reports detection difficulty by error type. Tested on annotation data instead (Section 1). |
| `analysis2` | Analysis 1: the fluency paradox | Directional findings, one contrary (Koponen et al. 2019) |
| `analysis3`, `analysis3b` | withdrawn | No verified data |
| `analysis4` | Analysis 2: over-editing concentration | Predicted negative τ in both sources with per-type rates; not significant |

The reasons for each withdrawal are recorded in `metadata.withdrawn_analyses` of
[all_results.json](outputs/retroactive_validation/all_results.json). The evidence
ledger counts findings from repository Analyses 2 and 4 only. Its headline counts
are written to [ledger_counts.tex](outputs/retroactive_validation/ledger_counts.tex)
as `\newcommand` macros (`\LedgerSources`, `\LedgerFindings`, `\LedgerSupport`, …),
which the paper `\input`s instead of restating the numbers.

**Superseded results.** Earlier versions of this repository (up to commit `705b8ed`)
reported a convergence ratio of 93.2–93.6 %, a pooled Analysis 1 p = 0.044, and
Analyses 3 and 3b. These rested on values the sources do not contain and should not
be cited. They remain in the history for audit. The convergence heatmap
(`F6_convergence_heatmap.png`, also circulated as `Fig4_Convergence.pdf`) showed the
withdrawn ratio, a "Partial" verdict and an expertise column for the withdrawn
Analysis 3; it was deleted in commit `30e68d0` rather than regenerated.

The camera-ready paper also withdraws the difficulty-gradient analysis and no
longer cites Daems et al. (2017) or Popović (2018), neither of which reports data
at the granularity that analysis required. Ledger counts in commits up to and
including `3baa684` therefore exceed those in the published paper.

---

## Reproducing the results

Requires Python 3.11. The R stages of the ToM hierarchy validation additionally need R
with `ordinal`, `lme4` and `jsonlite`; install them with
`Rscript experiments/tom_validation/install.R`. The committed results used R 4.2.3,
ordinal 2023.12.4 and lme4 1.1.35.3; re-running with R 4.6.1, ordinal 2026.7.26 and
lme4 2.0.6 changes the CLMM and GLMM estimates only in the fourth decimal place.

```bash
pip install -r requirements.txt

# ToM hierarchy validation
python scripts/fetch_wmt_mqm.py                       # download + verify the WMT data
python -m experiments.tom_validation.run_all          # add --skip-r without R

# Retroactive validation (no external data)
python -m experiments.retroactive_validation.run_all
python scripts/generate_retroactive_report.py         # rebuild the report from saved results
```

## Data

The WMT 2020 MQM annotations (Freitag et al., 2021, *Experts, Errors, and Context*,
TACL) are distributed by
[google/wmt-mqm-human-evaluation](https://github.com/google/wmt-mqm-human-evaluation)
under Apache 2.0. They are not redistributed here: `scripts/fetch_wmt_mqm.py`
downloads `newstest2020/ende/mqm_newstest2020_ende.tsv` at commit `9d2d6ca` and
verifies its SHA-256 against the copy the committed results were computed from.
Derived files (`tom_errors.csv`, `rater_level_data.csv`) are regenerated by the
pipeline and not tracked.

## Repository layout

```
experiments/
  tom_validation/          ToM hierarchy validation (Python + R)
  retroactive_validation/  Retroactive validation; data/published_data.py holds the verified values
outputs/
  tom_validation/          Results, figures, EXPERIMENTS.md
  retroactive_validation/  Results, figures, Experiment_Report.md
scripts/
  fetch_wmt_mqm.py         Download and verify the WMT 2020 MQM data
  generate_retroactive_report.py
```

## History and renamed paths

The code was developed in the ToM-PE repository, and its history for these paths
(from 2026-03-19) is merged into this one. Copies are currently kept in both
repositories.

| Old path | Current path |
|---|---|
| `experiments/ectel/` | `experiments/retroactive_validation/` |
| `outputs/ectel/ECTEL_Experiment_Report.md` | `outputs/retroactive_validation/Experiment_Report.md` |
| `outputs/ectel/no_temnikova/` | removed (superseded) |
| `scripts/generate_ectel_report.py` | `scripts/generate_retroactive_report.py` |
| Experiments 1–5 | Analyses 1, 2 and 4, plus the evidence ledger (former Experiment 5) |
