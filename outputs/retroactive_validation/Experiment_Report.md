# Retroactive Validation of the ToM Framework for Post-Editing

Detailed results report. Generated from `all_results.json` and `data/published_data.py`; do not edit by hand.

- **Generated:** 2026-10-05 20:32
- **Run timestamp:** 2026-10-05T20:32:39.393665
- **Data version:** published_data.py verified 2026-10
- **Tag:** `full`
- **Excluded sources:** none
- **Publication:** Diana Nurbakova and Liana Ermakova. 2026. *When Fluency Masks Failure: A Theory of Mind Model of Error Detection in Machine Translation Post-Editing.* In Proceedings of the IEEE/WIC International Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2026).

---

## 1. Summary

| Analysis | Status | Support | Mixed | Against | Uninformative | Sources |
|---|---|---|---|---|---|---|
| Analysis 1 | qualitative only | 2 | 0 | 0 | 0 | Daems2017, Popovic2018 |
| Analysis 2 | run | 5 | 1 | 1 | 0 | Bentivogli2018, Koponen2019, Popovic2018, VanBrussel2018, Yamada2019 |
| Analysis 4 | run | 2 | 1 | 0 | 1 | DeAlmeida2013, Koponen2015, Koponen2019, KoponenSalmi2017 |
| Analysis 3 | withdrawn |  |  |  |  | Expertise: no inferential source survives verification. |
| Analysis 3b | withdrawn |  |  |  |  | Development: Koponen (2015) contains no per-type or per-session data. |

- 13 findings from 9 distinct sources.
- 2 findings rest on an inferential test; 0 of them reach p < 0.05.
- Analysis 1 (difficulty ordering) has no quantitative test: no verified source reports detection difficulty by error type.
- **Analysis1_DifficultyOrdering**: NOT TESTED QUANTITATIVELY: no verified source reports difficulty by error type. Two qualitative findings are consistent with the ordering.
- **Analysis2_FluencyParadox**: 5 supporting, 1 mixed and 1 contrary findings from 5 sources. No finding rests on an inferential test.
- **Analysis4_OverEditing**: 2/2 sources with per-type rates show the predicted negative tau under both mappings; none is significant. Nitzke & Gros and Mellinger & Shreve are not counted until verified.

---

## 2. Data Revision (2026-10)

The source data were re-extracted from the full texts in October 2026. The earlier encoding required every source to yield per-category numbers on a comparable scale; where a source did not report in that shape, values were filled in. The verified module enforces three rules:

1. **No value without provenance.** Every numeric value names its table or page and the measure the source actually reports.
2. **Qualitative findings stay qualitative.** A direction reported without per-category figures is counted as a finding, never used as input to a correlation.
3. **Deletions are recorded.** Every dropped encoding is listed below with the reason.

### 2.1 Withdrawn encodings

| Encoding | Was | Reason | Replacement (in `published_data.py`) |
|---|---|---|---|
| Daems2017.fixation_rank | [1,2,3,4,5] for S1,S2,S3,S6,S7 — identical to ToM rank | No per-error-type difficulty ranking exists in the source. Fixation duration was not significantly predicted by MT quality at all; the authors suggest it may be a poor effort measure. tau=1.000 in Analyses 1 and 3 was arithmetic, not a finding. | Qualitative: grammatical errors predict technical and product effort; coherence and meaning shifts predict cognitive effort (fixations, duration). A dissociation along the hierarchy. |
| Koponen2015.performance_by_session | Five smooth monotone series over six sessions | The source is a course-description paper: 7 lectures, 5 assignments, thematic analysis of 13 reflective essays. It contains no per-type or per-session performance data and states that no detailed analysis of the students' edits was performed. | Qualitative only: students reported difficulty distinguishing PE quality levels and that they were likely correcting too much. |
| Koponen2019.measures[*].unnecessary_pct | word form 42, substitution 25, omission 10, insertion 45 | INVERTS the source. Table 5 gives insertions as the most necessary edit type (26% unnecessary) and order changes the least (59%). The encoded values produced tau=+0.183 and all three contradictions in the convergence table. | Verified rates above. |
| Koponen2019.measures[*].nmt_overlooked/smt_overlooked | Per-type counts 5/15/20/4/5 and 12/18/16/5/5 | The source reports system totals only (49/56/80). The decomposition was fabricated and reversed the source's aggregate direction. | System totals above, flagged as running against the prediction. |
| KoponenSalmi2017.measures[*].pct_of_unnecessary | 0.40/0.25/0.20/0.10/0.05, summing to exactly 1.00 | The source reports unnecessary RATES per edit type, not shares of a total, and has no style (S6) or discourse (S7) categories at all. | Verified rates above. |
| Bentivogli2018.measures[*].nmt_reduction_pct | Morphology 50, Reordering 45, Lexical 15, Omission/Addition -10 | Real reductions are -31.7/-41.4, -40.9/-48.4, -16.9/-27.1. The source has no omission/addition category, so the -10 value that carried the S4 claim does not exist. | Verified reductions above. |
| VanBrussel2018.measures[*].nmt_count/smt_count | 45/120, 38/95, 72/90, 35/30, 25/5 | Real counts differ throughout, and the encoded omission figures reversed the source: NMT has FEWER omissions than PBMT (62 vs 115), not more. | Verified counts and the omission-visibility data above. |
| Popovic2018.measures[*].nmt_rate/pbmt_rate | 0.12/0.25, 0.08/0.18, 0.22/0.28, 0.15/0.12, 0.20/0.22 | The source reports language-related issues per segment, not MQM error-category rates. No correspondence to the encoded categories. | Qualitative findings above. |
| Yamada2019.measures[*].nmt_correction/smt_correction | 0.78/0.82 (X4 Grammar), 0.62/0.75 (X1 Addition), 0.58/0.73 (X2 Omission), 0.65/0.76 (X3 Mistranslation) | The source reports error DISTRIBUTIONS (Figures 1-2), not correction rates by error type. It has three tables only: effort, raw error counts, and overall PE quality. The old header cited 'Tables 4-6', which do not exist. The category labels were also wrong: X2 is content addition, not omission, and there is no 'X4 Grammar' (X4a is untranslated, X4b too literal, X9 syntax). | Aggregate correction rates 0.777 and 0.68, plus qualitative findings. Removes Yamada from Analysis 1 entirely. |
| DeAlmeida2013.measures[*].experienced_rate/novice_rate | 0.85/0.60 (S3) and 0.70/0.55 (S1) | The thesis reports proportions of item categories, not per-experience rates by ToM proxy. | Verified aggregates above. |

Results produced from the earlier encoding (the former convergence table, the Analysis 1 rank correlations, Analyses 3 and 3b) are superseded and should not be cited. They remain in the git history for audit.

---

## 3. Framework: MQM-to-ToM Mapping

| Skill | ToM level | Rank | MQM categories |
|---|---|---|---|
| S1 Surface | 1st_machine (form) | 1 | Spelling, Punctuation |
| S2 Grammar | 1st_machine (form) | 2 | Grammar, Word form |
| S3 Meaning | 1st_machine (meaning) | 3 | Mistranslation, Wrong sense, False cognate, Number |
| S4 Completeness | 1st_author | 4 | Omission, Addition, Untranslated |
| S5 Terminology | 2nd_reader | 4 | Terminology |
| S6 Pragmatic | 2nd_reader | 4 | Register, Style, Locale |
| S7 Discourse | recursive | 5 | Coherence, Cohesion, Connectives |

- Ordinal scale: S1=1, S2=2, S3=3, S4=S5=S6=4 (tied), S7=5.
- Low-ToM = S1–S2; high-ToM = S3 and above.
- Mapping sensitivity: The edit type 'deleted' has two defensible ToM assignments. In both sources most deletions are optional subject pronouns, which is a target-language grammar matter (S2); but deletion removes content, which bears on completeness (S4). Both assignments are reported for Analysis 4.

---

## 4. Sources

### 4.1 Verified sources

| Source | Citation | Pairs | Participants | Measure |
|---|---|---|---|---|
| Bentivogli2018 | Bentivogli, Bisazza, Cettolo & Federico (2018), Computer Speech & Language 49:52-70 | EN-DE, EN-FR | — | relative error reduction, NMT vs PBMT, from HTER-based error classes |
| DeAlmeida2013 | de Almeida (2013), doctoral thesis, Dublin City University | EN-FR, EN-PT-BR | 20 | proportion of recorded items by change category |
| Koponen2019 | Koponen, Salmi & Nikulin (2019), Machine Translation 33(1-2):61-90 | EN-FI | 33 students | proportion of edits of this type correct but unnecessary |
| KoponenSalmi2017 | Koponen & Salmi (2017), Linguistica Antverpiensia 16:137-148 | EN-FI | 5 students | proportion of edits of this type judged unnecessary |
| Popovic2018 | Popović (2018), Machine Translation 32(3):237-253 | DE-EN, EN-DE, EN-SR | — | language-related issues per segment — NOT MQM error categories |
| VanBrussel2018 | Van Brussel, Tezcan & Macken (2018), LREC 2018 | EN-NL | — | annotated error counts by category |
| Yamada2019 | Yamada (2019), The Journal of Specialised Translation 31:87-106 | EN-JA | 28 students | error correction rate, major errors only |

### 4.2 Assignment to analyses

| Analysis | Sources |
|---|---|
| analysis_1_difficulty | Daems2017 (qualitative), Popovic2018 (qualitative) |
| analysis_2_fluency | Yamada2019, Bentivogli2018, VanBrussel2018, Popovic2018 (qualitative), Koponen2019 (AGAINST) |
| analysis_3_expertise | none (withdrawn) |
| analysis_3b_development | none (withdrawn) |
| analysis_4_overediting | KoponenSalmi2017, Koponen2019, DeAlmeida2013, NitzkeGros2020 (aggregates only), MellingerShreve2016 (aggregates only), Koponen2015 (qualitative) |

### 4.3 Not verified, not counted

| Source | Status |
|---|---|
| NitzkeGros2020 | Aggregates (1 unnecessary change per 22.3 words; 45.16 preferential per 1008 words) look transcribed. The per-category shares 0.30/0.35/0.20/0.10/0.05 sum to exactly 1.00 and follow the fabrication signature. Do not use the shares. |
| MellingerShreve2016 | 60% of exact TM matches changed; 74% of fuzzy matches corrected. Look transcribed; unread. |
| Stasimioti2021 | Contributes no per-type data. Reference not located; not cited in the paper. |
| Temnikova2010 | Excluded for construct mismatch (correction effort, not detection). |

---

## 5. Analysis 1: ToM Ordering vs. Detection Difficulty

**Prediction.** Higher-ToM error types are harder to detect.

**Status.** Qualitative only. The rank correlations reported previously rested on values withdrawn in Section 2.1 (Daems fixation ranks, Yamada per-type correction rates, Popović category rates, Temnikova ranks).

| Source | Direction | Basis | Finding | Location |
|---|---|---|---|---|
| Daems2017 | support | qualitative | Qualitative: grammatical errors predict technical and product effort; coherence and meaning shifts predict cognitive effort (fixations, duration). A dissociation along the hierarchy. | Daems et al. (2017), regression models by error type |
| Popovic2018 | support | qualitative | NMT is worse than PBMT on ambiguous source words (S3) in every direction while better on verb forms and order (S2). | Table 2 |

**Interpretation.** NOT TESTED QUANTITATIVELY: no verified source reports difficulty by error type. Two qualitative findings are consistent with the ordering.

---

## 6. Analysis 2: Fluency Paradox

**Prediction.** NMT reduces low-ToM errors more than high-ToM errors, and post-editors catch fewer of the errors that remain.

**Method.** For sources with verified per-category error data, each high-ToM category's relative error change under NMT is compared with the mean low-ToM change. A source supports the prediction if every high-ToM category fell less than the low-ToM categories (or rose), contradicts it if none did, and is mixed otherwise. Aggregate and qualitative findings are recorded with the direction the source reports. No inferential test is applied: per-category counts from one corpus are not independent observations.

### 6.1 Findings

| Source | Direction | Basis | Finding | Location |
|---|---|---|---|---|
| Yamada2019 | support | numeric descriptive | Students corrected 77.7% of major errors in SMT output but 68% in NMT output. | Table 3 |
| Bentivogli2018 | support | numeric descriptive | NMT reduced word-order and morphology errors (S2) more than lexical errors (S3), in both language pairs. | Section 5 and Conclusions |
| Bentivogli2018 | support | numeric descriptive | Lexical errors' share of residual errors rises from PBMT to NMT (EnDe 72.1% -> 76.9%, EnFr 74.5% -> 79.0%). | Section 5 |
| VanBrussel2018 | mixed | numeric descriptive | Error counts NMT vs PBMT: grammar (S2) fell 72%; 4/5 high-ToM categories fell less or rose (exception: addition). | Tables 1, 3, 4, 7, 9 |
| VanBrussel2018 | support | numeric descriptive | Omissions with no trace in the target: RBMT 7%, PBMT 23%, NMT 69%. In NMT, fluency no longer signals that source content is missing. | Table 6 |
| Popovic2018 | support | qualitative | NMT better on verb forms, order, compounds; worse on prepositions and ambiguous source words in every direction. | Table 2 |
| Koponen2019 | against | numeric descriptive | Overlooked necessary corrections: NMT 2.2%, SMT 2.7%, RBMT 3.3% of unedited words. NMT has the fewest. | Section 4.1, closing paragraph |

### 6.2 Bentivogli et al. (2018): relative error change, NMT vs PBMT

| Pair | Error class | Skill | Change |
|---|---|---|---|
| EnDe | Word order | S2 | -41% |
| EnDe | Morphology | S2 | -32% |
| EnDe | Lexical | S3 | -17% |
| EnFr | Word order | S2 | -48% |
| EnFr | Morphology | S2 | -41% |
| EnFr | Lexical | S3 | -27% |

Caveat: The source uses three coarse classes only (lexical, morphology, word order) and folds missing and extra words into 'lexical'. There is no omission/addition category, so no S4 value can be taken from it.

### 6.3 Van Brussel et al. (2018): error counts by category

| Category | Skill | RBMT | PBMT | NMT | NMT vs PBMT | NMT vs RBMT |
|---|---|---|---|---|---|---|
| fluency_grammar | S2 | 864 | 932 | 260 | -72% | -70% |
| fluency_lexicon | S3 | 533 | 235 | 358 | +52% | -33% |
| mistranslation | S3 | 972 | 483 | 330 | -32% | -66% |
| semantically_unrelated | S3 | 0 | 9 | 44 | +389% | new (from 0) |
| omission | S4 | 43 | 115 | 62 | -46% | +44% |
| addition | S4 | 61 | 39 | 2 | -95% | -97% |

Against PBMT (primary): mixed. Against RBMT (secondary, not counted): mixed.

**Interpretation.** 5 supporting, 1 mixed and 1 contrary findings from 5 sources. No finding rests on an inferential test.

*Contrary evidence (Koponen2019).* NMT has the FEWEST overlooked necessary corrections. At the only level the source reports, this runs counter to the fluency-paradox prediction. Report it; do not drop it.

---

## 7. Analyses 3 and 3b: Withdrawn

- **Analysis 3.** Expertise: no inferential source survives verification.
- **Analysis 3b.** Development: Koponen (2015) contains no per-type or per-session data.

---

## 8. Analysis 4: Over-Editing as Misdirected ToM

**Prediction.** Unnecessary edits concentrate on low-ToM types; negative tau between ToM rank and unnecessary-edit rate.

**Method.** For sources reporting the rate at which edits of each type were unnecessary, Kendall's τ-b between ToM rank and that rate (two-sided p). Deletions are assigned to S2 (primary) and to S4 (alternative); both are reported.

### 8.1 Findings

| Source | Direction | Basis | Finding | Location |
|---|---|---|---|---|
| KoponenSalmi2017 | support | numeric test | Unnecessary-edit rate falls with ToM rank (deleted=S2: tau=-0.598, p=0.166, deleted=S4: tau=-0.224, p=0.602); not significant under either mapping. Ranks span S2-S4 only. | Section 5, Discussion |
| Koponen2019 | support | numeric test | Unnecessary-edit rate falls with ToM rank (deleted=S2: tau=-0.598, p=0.166, deleted=S4: tau=-0.224, p=0.602); not significant under either mapping. Ranks span S2-S4 only. | Table 5, NMT panel |
| DeAlmeida2013 | mixed | numeric descriptive | Preferential changes were 15.59% (EN-PT-BR) to 24.56% (EN-FR) of recorded items; the most experienced translators made the most preferential changes. | Sections 4.9.1 and 4.9.2 (pp. 191-195) |
| Koponen2015 | uninformative | qualitative | Qualitative only: students reported difficulty distinguishing PE quality levels and that they were likely correcting too much. | Koponen (2015), thematic analysis of reflective essays |

### 8.2 Rank correlations under both mappings

| Source | Mapping | n | τ | p |
|---|---|---|---|---|
| KoponenSalmi2017 | deleted = S2 | 5 | -0.598 | 0.166 |
| KoponenSalmi2017 | deleted = S4 | 5 | -0.224 | 0.602 |
| Koponen2019 | deleted = S2 | 5 | -0.598 | 0.166 |
| Koponen2019 | deleted = S4 | 5 | -0.224 | 0.602 |

### 8.3 Per-type unnecessary-edit rates

| Source | Edit type | Skill (primary) | Unnecessary | Edits |
|---|---|---|---|---|
| KoponenSalmi2017 | Word-order changes | S2 | 80% | — |
| KoponenSalmi2017 | Deletions | S2 | 70% | — |
| KoponenSalmi2017 | Word substitutions | S3 | 33% | — |
| KoponenSalmi2017 | Word-form changes | S2 | 30% | — |
| KoponenSalmi2017 | Insertions | S4 | 16% | — |
| Koponen2019 | Order changed | S2 | 59% | 123 |
| Koponen2019 | Deleted | S2 | 38% | 290 |
| Koponen2019 | Word substituted | S3 | 35% | 404 |
| Koponen2019 | Form changed | S2 | 32% | 493 |
| Koponen2019 | Inserted | S4 | 26% | 357 |

Note: Identical for both sources, because the two studies produce the same ordering of edit types by unnecessary rate. Report both mappings; the result is directionally stable and neither is significant. Ranks span S2–S4 only; neither source has S1, S5–S7 categories.

**Interpretation.** 2/2 sources with per-type rates show the predicted negative tau under both mappings; none is significant. Nitzke & Gros and Mellinger & Shreve are not counted until verified.

---

## 9. Evidence Ledger

The ledger replaces the former category-by-analysis convergence table and its convergence ratio. Findings differ in basis and measure, so they are counted, not pooled, and no ratio or binomial test is computed.

| Direction | numeric test | numeric descriptive | qualitative | Total |
|---|---|---|---|---|
| support | 2 | 4 | 3 | 9 |
| mixed | 0 | 2 | 0 | 2 |
| against | 0 | 1 | 0 | 1 |
| uninformative | 0 | 0 | 1 | 1 |

Counts of findings, not of independent tests. A source can contribute more than one finding, and to more than one analysis.

Sources contributing to more than one analysis: Koponen2019, Popovic2018.

---

## 10. Limitations

- Only 2 findings rest on an inferential test, and none reaches significance. The retrospective evidence is directional, not confirmatory.
- The difficulty gradient (Analysis 1) has no quantitative support in the verified literature.
- Measures differ between sources and are not commensurable; directions are compared, magnitudes are not.
- Nitzke & Gros (2020) and Mellinger & Shreve (2016) are excluded pending verification; Stasimioti & Sosoni (2021) contributes no data.
- The direction rule in Analysis 2 counts consistent comparisons; it does not weight categories by size.

---

## 11. Outputs and Reproducibility

| File | Contents |
|---|---|
| `all_results.json` | Structured results for every analysis and the ledger |
| `Experiment_Report.md` | This report |
| `F5_fluency_paradox.pdf` (+ `.png`) | Analysis 2: relative error change by category; omission visibility |
| `F7_overediting.pdf` (+ `.png`) | Analysis 4: unnecessary-edit rate by edit type, both mappings |

```bash
python -m experiments.retroactive_validation.run_all            # full run, writes this report
python -m experiments.retroactive_validation.run_all --exclude Koponen2019   # sensitivity
python scripts/generate_retroactive_report.py                    # rebuild report from JSON
```

Environment at generation: Python 3.11.9, SciPy 1.17.1, NumPy 1.26.4, Matplotlib 3.10.8.
