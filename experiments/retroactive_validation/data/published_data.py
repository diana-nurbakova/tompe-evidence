"""Published empirical data, re-extracted from source publications (2026-10).

This module replaces `published_data.py`. The previous version encoded
per-category values for every source. Re-reading the sources showed that most
of those values were numeric instantiations of qualitative statements, and some
inverted what the source reported. The root cause was schematic: the old module
required every source to yield per-category numbers on a comparable scale, so
sources that did not report in that shape had values invented to fill it.

Three structural rules follow from that, and they are enforced here:

1. NO VALUE WITHOUT PROVENANCE. Every numeric value carries `source_location`
   (table or page) and `measure` (what the source actually measured). A value
   that cannot name both does not belong in this file.

2. QUALITATIVE FINDINGS STAY QUALITATIVE. Where a source reports a direction but
   no per-category figures, it is recorded under `qualitative` as the finding,
   not converted into numbers. Analyses must handle these as counts of
   direction-consistent findings, never as inputs to a correlation.

3. DELETIONS ARE RECORDED, NOT REMOVED. `DELETED` documents every encoding that
   was dropped and why, so the change is auditable against the old results.

Measures differ between sources and are NOT commensurable. `measure` must be
checked before any value is compared across sources.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# VERIFIED SOURCES
# ---------------------------------------------------------------------------

KOPONEN_SALMI_2017 = {
    "source": "KoponenSalmi2017",
    "citation": "Koponen & Salmi (2017), Linguistica Antverpiensia 16:137-148",
    "verified": "2026-10, full text",
    "n_participants": {"students": 5},
    "language_pair": "EN-FI",
    "design": "light PE, 27 segments (385 words), MT from RBMT+SMT+NMT, 1715 words analysed",
    "aggregate": {
        "edits_total": 679,
        "edits_correct": 620,
        "unnecessary_pct_of_all_edits": 34,
        "unnecessary_pct_of_correct_edits": 38,
        "source_location": "abstract (34%), Section 6 (38%), Table 3",
        "note": "The source gives both figures on different denominators "
                "(235/679 and 235/620). Cite with the denominator stated.",
    },
    # VERIFIED: unnecessary RATE per edit type. Not shares of a total.
    "measure": "proportion of edits of this type judged unnecessary",
    "source_location": "Section 5, Discussion",
    "measures": [
        {"edit_type": "Word-order changes", "skill": "S2", "unnecessary_rate": 0.80},
        {"edit_type": "Deletions",          "skill": "S2", "unnecessary_rate": 0.70,
         "note": "mostly optional subject pronouns; see MAPPING_SENSITIVITY"},
        {"edit_type": "Word substitutions", "skill": "S3", "unnecessary_rate": 0.33},
        {"edit_type": "Word-form changes",  "skill": "S2", "unnecessary_rate": 0.30},
        {"edit_type": "Insertions",         "skill": "S4", "unnecessary_rate": 0.16},
    ],
    "qualitative": [
        "Punctuation changes generally unnecessary.",
        "Word-order changes largely stylistic, attributed to free Finnish word order.",
    ],
}

KOPONEN_2019 = {
    "source": "Koponen2019",
    "citation": "Koponen, Salmi & Nikulin (2019), Machine Translation 33(1-2):61-90",
    "verified": "2026-10, full text",
    "n_participants": {"students": 33},
    "language_pair": "EN-FI",
    "mt_systems": ["NMT", "SMT", "RBMT"],
    "measure": "proportion of edits of this type correct but unnecessary",
    "source_location": "Table 5, NMT panel",
    "measures": [
        {"edit_type": "Order changed",    "skill": "S2", "total": 123, "unnecessary_rate": 0.59},
        {"edit_type": "Deleted",          "skill": "S2", "total": 290, "unnecessary_rate": 0.38,
         "note": "see MAPPING_SENSITIVITY"},
        {"edit_type": "Word substituted", "skill": "S3", "total": 404, "unnecessary_rate": 0.35},
        {"edit_type": "Form changed",     "skill": "S2", "total": 493, "unnecessary_rate": 0.32},
        {"edit_type": "Inserted",         "skill": "S4", "total": 357, "unnecessary_rate": 0.26},
    ],
    # VERIFIED: overlooked corrections are SYSTEM TOTALS ONLY. No per-type data.
    "overlooked": {
        "measure": "cases where an edit would have been necessary, as % of unedited words",
        "source_location": "Section 4.1, closing paragraph",
        "NMT": {"count": 49, "pct_of_unedited": 2.2},
        "SMT": {"count": 56, "pct_of_unedited": 2.7},
        "RBMT": {"count": 80, "pct_of_unedited": 3.3},
        "per_category_breakdown": None,
        "bears_on_prediction": "AGAINST",
        "note": "NMT has the FEWEST overlooked necessary corrections. At the only "
                "level the source reports, this runs counter to the fluency-paradox "
                "prediction. Report it; do not drop it.",
    },
    "qualitative": [
        "Most edits to RBMT output unnecessary even if correct (61%); NMT and SMT mostly necessary (60%, 67%).",
        "Unnecessary edits in RBMT connected to 2nd person forms and subject pronouns.",
        "NMT output: fewest word-order errors, most lexical errors (substitutions).",
    ],
}

VAN_BRUSSEL_2018 = {
    "source": "VanBrussel2018",
    "citation": "Van Brussel, Tezcan & Macken (2018), LREC 2018",
    "verified": "2026-10, full text",
    "language_pair": "EN-NL",
    "design": "SCATE corpus, 665 sentences, RBMT (Systran) / PBMT (Google) / NMT (GNMT)",
    "error_counts": {
        "measure": "annotated error counts by category",
        "source_location": "Tables 1, 3, 4, 7, 9",
        "fluency_grammar":   {"RBMT": 864,  "PBMT": 932,  "NMT": 260, "skill": "S2"},
        "fluency_lexicon":   {"RBMT": 533,  "PBMT": 235,  "NMT": 358, "skill": "S3",
                              "note": "NMT WORSE: lexical choice content words 91 -> 226"},
        "mistranslation":    {"RBMT": 972,  "PBMT": 483,  "NMT": 330, "skill": "S3"},
        "semantically_unrelated": {"RBMT": 0, "PBMT": 9,  "NMT": 44,  "skill": "S3",
                              "note": "new category; absent from RBMT, rare in PBMT"},
        "omission":          {"RBMT": 43,   "PBMT": 115,  "NMT": 62,  "skill": "S4"},
        "addition":          {"RBMT": 61,   "PBMT": 39,   "NMT": 2,   "skill": "S4"},
    },
    # The paper's most important finding for ToM-PE, and unused in the old encoding.
    "omission_visibility": {
        "measure": "proportion of omissions with no trace in the target text, "
                   "i.e. undetectable without consulting the source",
        "source_location": "Table 6",
        "RBMT": 0.07, "PBMT": 0.23, "NMT": 0.69,
        "content_word_share": {"RBMT": 0.0014, "PBMT": 0.6996, "NMT": 0.8548},
        "words_per_omission": {"RBMT": 1.07, "PBMT": 1.09, "NMT": 1.50},
        "bears_on_prediction": "DIRECT SUPPORT",
        "note": "The source states that in RBMT and PBMT output omissions are "
                "anticipated by fluency errors, whereas in NMT fluency is no "
                "indicator that source content transferred. This is a direct "
                "measurement of the mechanism ToM-PE posits: fluency removes the "
                "surface cue that would trigger the higher-order check.",
    },
}

BENTIVOGLI_2018 = {
    "source": "Bentivogli2018",
    "citation": "Bentivogli, Bisazza, Cettolo & Federico (2018), Computer Speech & Language 49:52-70",
    "verified": "2026-10, full text",
    "language_pairs": ["EN-DE", "EN-FR"],
    "measure": "relative error reduction, NMT vs PBMT, from HTER-based error classes",
    "source_location": "Section 5 and Conclusions",
    "measures": [
        {"error_class": "Word order",  "skill": "S2", "reduction_EnDe": -40.9, "reduction_EnFr": -48.4},
        {"error_class": "Morphology",  "skill": "S2", "reduction_EnDe": -31.7, "reduction_EnFr": -41.4},
        {"error_class": "Lexical",     "skill": "S3", "reduction_EnDe": -16.9, "reduction_EnFr": -27.1},
    ],
    "overall_reduction": {"EnDe": -22.0, "EnFr": -31.2},
    "lexical_share_of_residual_errors": {
        "measure": "lexical errors as % of all errors",
        "source_location": "Section 5",
        "EnDe": {"PBMT": 72.1, "NMT": 76.9},
        "EnFr": {"PBMT": 74.5, "NMT": 79.0},
        "bears_on_prediction": "SUPPORT",
        "note": "As output improves, the residual error profile shifts toward "
                "meaning-level errors.",
    },
    "no_completeness_category": True,
    "note": "The source uses three coarse classes only (lexical, morphology, word "
            "order) and folds missing and extra words into 'lexical'. There is no "
            "omission/addition category, so no S4 value can be taken from it.",
}

POPOVIC_2018 = {
    "source": "Popovic2018",
    "citation": "Popović (2018), Machine Translation 32(3):237-253",
    "verified": "2026-10, full text",
    "language_pairs": ["DE-EN", "EN-DE", "EN-SR"],
    "measure": "language-related issues per segment — NOT MQM error categories",
    "source_location": "Table 2",
    "measures": None,
    "qualitative": {
        "nmt_better": ["verb forms", "verb omissions", "verb order (DE-EN)",
                       "English noun collocations and German compounds", "negation"],
        "nmt_worse": ["mistranslated prepositions (all directions)",
                      "ambiguous source words (all directions)",
                      "English continuous and perfect tenses"],
        "bears_on_prediction": "SUPPORT, qualitative",
        "note": "Ambiguous-word translation is a word-sense problem (S3) and NMT is "
                "worse at it in every direction, while improving on morphology and "
                "order (S2). The asymmetry is in the predicted direction, but the "
                "source reports no MQM-category rates, so no value is encoded.",
    },
}

DE_ALMEIDA_2013 = {
    "source": "DeAlmeida2013",
    "citation": "de Almeida (2013), doctoral thesis, Dublin City University",
    "verified": "2026-10, full text, Sections 4.9.1-4.9.2",
    "language_pairs": ["EN-FR", "EN-PT-BR"],
    "n_participants": 20,
    "measure": "proportion of recorded items by change category",
    "source_location": "Sections 4.9.1 and 4.9.2 (pp. 191-195)",
    "aggregate": {
        "EN-FR":    {"essential": 60.12, "preferential": 24.56, "not_implemented_plus_introduced": 15.31},
        "EN-PT-BR": {"essential": 63.97, "preferential": 15.59, "not_implemented_plus_introduced": 20.41},
        "essential_dominated_by_language_category": {"EN-FR": 54.98, "EN-PT-BR": 71.69},
    },
    "qualitative": [
        "The most experienced translators made both the most essential and the most "
        "preferential changes.",
    ],
    "bears_on_prediction": "MIXED",
    "note": "The preferential-change range (15.6% to 24.6%) supports the over-editing "
            "claim. The experience finding complicates it: over-editing is not purely "
            "a novice behaviour. State both.",
}

YAMADA_2019 = {
    "source": "Yamada2019",
    "citation": "Yamada (2019), The Journal of Specialised Translation 31:87-106",
    "verified": "2026-10, full text",
    "n_participants": {"students": 28},
    "language_pair": "EN-JA",
    "mt_systems": {"NMT": "Google NMT", "SMT": "Moses (Yamada 2014 replication)"},
    "error_taxonomy": "MNH-TT revision categories (X1-X14), not MQM",
    # VERIFIED aggregates. These are the only correction figures the source reports.
    "aggregate": {
        "measure": "error correction rate, major errors only",
        "source_location": "Table 3",
        "SMT_PE": {"correction_rate": 0.777, "range": [0.41, 0.93], "uncorrected_mean": 6.9},
        "NMT_PE": {"correction_rate": 0.68,  "range": [0.40, 0.90], "uncorrected_mean": 3.20},
        "bears_on_prediction": "DIRECT SUPPORT",
        "note": "Correction rate FELL from 77.7% to 68% when output improved. The "
                "source calls this result remarkable. This is the fluency paradox in "
                "a single figure, and it is the paper's headline finding.",
    },
    "raw_output_quality": {
        "source_location": "Table 2 and Section 5.3",
        "note": "Raw SMT contains 1.5x more errors than raw NMT; 72% of SMT errors "
                "are major against 37% for NMT. Students corrected a smaller "
                "proportion of a smaller and less severe error set.",
    },
    # The source reports error DISTRIBUTIONS, not per-type correction rates.
    "measures": None,
    "qualitative": [
        "X3 (content distortion / mistranslation) is the most frequent error type in "
        "raw NMT, raw SMT and student human translation alike.",
        "Raw SMT contains many error types (X4a untranslated, X4b too literal, X7 "
        "terminology, X9 syntax, X10 preposition) that are easy for humans to detect "
        "and modify.",
        "The NMT error pattern is roughly identical to that of human translators and "
        "therefore lacks a complementary relationship with the post-editor. This "
        "accounts for NMT+PE requiring similar total effort as SMT+PE despite fewer "
        "errors in the raw output.",
    ],
    "bears_on_prediction": "DIRECT SUPPORT, Analysis 2 only",
    "note": "NOT an Analysis 1 source. The paper reports error distributions "
            "(Figures 1-2), not correction rates by error type.",
}

# ---------------------------------------------------------------------------
# NOT YET VERIFIED — treat as qualitative until read
# ---------------------------------------------------------------------------

UNVERIFIED = {
    "NitzkeGros2020": "Aggregates (1 unnecessary change per 22.3 words; 45.16 "
                      "preferential per 1008 words) look transcribed. The per-category "
                      "shares 0.30/0.35/0.20/0.10/0.05 sum to exactly 1.00 and follow "
                      "the fabrication signature. Do not use the shares.",
    "MellingerShreve2016": "60% of exact TM matches changed; 74% of fuzzy matches "
                           "corrected. Look transcribed; unread.",
    "Stasimioti2021": "Contributes no per-type data. Reference not located; not cited "
                      "in the paper.",
    "Temnikova2010": "Excluded for construct mismatch (correction effort, not detection).",
}

# ---------------------------------------------------------------------------
# DELETED ENCODINGS — recorded for audit against the previous results
# ---------------------------------------------------------------------------

DELETED = {
    "Daems2017.fixation_rank": {
        "was": "[1,2,3,4,5] for S1,S2,S3,S6,S7 — identical to ToM rank",
        "reason": "No per-error-type difficulty ranking exists in the source. Fixation "
                  "duration was not significantly predicted by MT quality at all; the "
                  "authors suggest it may be a poor effort measure. tau=1.000 in "
                  "Analyses 1 and 3 was arithmetic, not a finding.",
        "replacement": "Qualitative: grammatical errors predict technical and product "
                       "effort; coherence and meaning shifts predict cognitive effort "
                       "(fixations, duration). A dissociation along the hierarchy.",
    },
    "Koponen2015.performance_by_session": {
        "was": "Five smooth monotone series over six sessions",
        "reason": "The source is a course-description paper: 7 lectures, 5 assignments, "
                  "thematic analysis of 13 reflective essays. It contains no per-type "
                  "or per-session performance data and states that no detailed analysis "
                  "of the students' edits was performed.",
        "replacement": "Qualitative only: students reported difficulty distinguishing "
                       "PE quality levels and that they were likely correcting too much.",
    },
    "Koponen2019.measures[*].unnecessary_pct": {
        "was": "word form 42, substitution 25, omission 10, insertion 45",
        "reason": "INVERTS the source. Table 5 gives insertions as the most necessary "
                  "edit type (26% unnecessary) and order changes the least (59%). The "
                  "encoded values produced tau=+0.183 and all three contradictions in "
                  "the convergence table.",
        "replacement": "Verified rates above.",
    },
    "Koponen2019.measures[*].nmt_overlooked/smt_overlooked": {
        "was": "Per-type counts 5/15/20/4/5 and 12/18/16/5/5",
        "reason": "The source reports system totals only (49/56/80). The decomposition "
                  "was fabricated and reversed the source's aggregate direction.",
        "replacement": "System totals above, flagged as running against the prediction.",
    },
    "KoponenSalmi2017.measures[*].pct_of_unnecessary": {
        "was": "0.40/0.25/0.20/0.10/0.05, summing to exactly 1.00",
        "reason": "The source reports unnecessary RATES per edit type, not shares of a "
                  "total, and has no style (S6) or discourse (S7) categories at all.",
        "replacement": "Verified rates above.",
    },
    "Bentivogli2018.measures[*].nmt_reduction_pct": {
        "was": "Morphology 50, Reordering 45, Lexical 15, Omission/Addition -10",
        "reason": "Real reductions are -31.7/-41.4, -40.9/-48.4, -16.9/-27.1. The "
                  "source has no omission/addition category, so the -10 value that "
                  "carried the S4 claim does not exist.",
        "replacement": "Verified reductions above.",
    },
    "VanBrussel2018.measures[*].nmt_count/smt_count": {
        "was": "45/120, 38/95, 72/90, 35/30, 25/5",
        "reason": "Real counts differ throughout, and the encoded omission figures "
                  "reversed the source: NMT has FEWER omissions than PBMT (62 vs 115), "
                  "not more.",
        "replacement": "Verified counts and the omission-visibility data above.",
    },
    "Popovic2018.measures[*].nmt_rate/pbmt_rate": {
        "was": "0.12/0.25, 0.08/0.18, 0.22/0.28, 0.15/0.12, 0.20/0.22",
        "reason": "The source reports language-related issues per segment, not MQM "
                  "error-category rates. No correspondence to the encoded categories.",
        "replacement": "Qualitative findings above.",
    },
    "Yamada2019.measures[*].nmt_correction/smt_correction": {
        "was": "0.78/0.82 (X4 Grammar), 0.62/0.75 (X1 Addition), 0.58/0.73 "
               "(X2 Omission), 0.65/0.76 (X3 Mistranslation)",
        "reason": "The source reports error DISTRIBUTIONS (Figures 1-2), not "
                  "correction rates by error type. It has three tables only: effort, "
                  "raw error counts, and overall PE quality. The old header cited "
                  "'Tables 4-6', which do not exist. The category labels were also "
                  "wrong: X2 is content addition, not omission, and there is no "
                  "'X4 Grammar' (X4a is untranslated, X4b too literal, X9 syntax).",
        "replacement": "Aggregate correction rates 0.777 and 0.68, plus qualitative "
                       "findings. Removes Yamada from Analysis 1 entirely.",
    },
    "DeAlmeida2013.measures[*].experienced_rate/novice_rate": {
        "was": "0.85/0.60 (S3) and 0.70/0.55 (S1)",
        "reason": "The thesis reports proportions of item categories, not per-experience "
                  "rates by ToM proxy.",
        "replacement": "Verified aggregates above.",
    },
}

# ---------------------------------------------------------------------------
# MAPPING SENSITIVITY — must be reported with any Analysis 4 result
# ---------------------------------------------------------------------------

MAPPING_SENSITIVITY = {
    "issue": "The edit type 'deleted' has two defensible ToM assignments. In both "
             "sources most deletions are optional subject pronouns, which is a "
             "target-language grammar matter (S2); but deletion removes content, "
             "which bears on completeness (S4).",
    "effect_on_analysis_4": {
        "deleted=S2": {"tau": -0.598, "p": 0.166},
        "deleted=S4": {"tau": -0.224, "p": 0.602},
    },
    "note": "Identical for both sources, because the two studies produce the same "
            "ordering of edit types by unnecessary rate. Report both mappings; the "
            "result is directionally stable and neither is significant.",
}

EXPERIMENT_SOURCES = {
    # NO numeric source survives. The difficulty gradient has no quantitative
    # support in the retrospective literature; only the 46K analysis tests it.
    "analysis_1_difficulty":   ["Daems2017 (qualitative)", "Popovic2018 (qualitative)"],
    "analysis_2_fluency":      ["Yamada2019", "Bentivogli2018", "VanBrussel2018",
                                "Popovic2018 (qualitative)", "Koponen2019 (AGAINST)"],
    "analysis_3_expertise":    [],   # deleted: no inferential source survives
    "analysis_3b_development": [],   # deleted: source contains no such data
    "analysis_4_overediting":  ["KoponenSalmi2017", "Koponen2019", "DeAlmeida2013",
                                "NitzkeGros2020 (aggregates only)",
                                "MellingerShreve2016 (aggregates only)",
                                "Koponen2015 (qualitative)"],
}
