"""Analysis 1: ToM ordering vs. detection difficulty.

Prediction: error types requiring higher-order ToM are harder to detect.

No verified source reports a per-error-type difficulty measure, so no
correlation is computed. The former Kendall tau inputs (Daems fixation ranks,
Yamada per-type correction rates, Popovic per-category rates, Temnikova ranks)
were withdrawn; see `published_data.DELETED`. What remains is qualitative.
"""

from __future__ import annotations

from typing import Dict

from .data import published_data as pd
from .evidence_ledger import QUALITATIVE, SUPPORT, finding

ANALYSIS = "Analysis 1"


def run_all() -> Dict:
    daems = pd.DELETED["Daems2017.fixation_rank"]
    popovic = pd.POPOVIC_2018["qualitative"]

    findings = [
        finding(
            ANALYSIS, "Daems2017",
            daems["replacement"],
            SUPPORT, QUALITATIVE,
            "Daems et al. (2017), regression models by error type",
            {"caveat": daems["reason"]},
        ),
        finding(
            ANALYSIS, "Popovic2018",
            "NMT is worse than PBMT on ambiguous source words (S3) in every "
            "direction while better on verb forms and order (S2).",
            SUPPORT, QUALITATIVE,
            pd.POPOVIC_2018["source_location"],
            {"nmt_better": popovic["nmt_better"], "nmt_worse": popovic["nmt_worse"],
             "caveat": popovic["note"]},
        ),
    ]

    return {
        "experiment": "Analysis1_DifficultyOrdering",
        "prediction": "Higher-ToM error types are harder to detect",
        "status": "qualitative only",
        "findings": findings,
        "interpretation": ("NOT TESTED QUANTITATIVELY: no verified source reports "
                           "difficulty by error type. Two qualitative findings are "
                           "consistent with the ordering."),
    }
