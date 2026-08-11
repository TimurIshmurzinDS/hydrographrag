#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HydroGraphRAG final OOD metrics evaluator.

Purpose
-------
Compute OOD rejection metrics from the frozen benchmark and the structured
ANSWER / ABSTAIN decision produced by each architecture.

Important evaluation policy
---------------------------
1. OOD ground truth comes from frozen ground_truth.json:
      expected_decision == "ABSTAIN"
   Valid in-domain ground truth:
      expected_decision == "ANSWER"

2. The OOD metric NEVER infers abstention from:
      - missing .py files
      - execution success/failure
      - syntax status
      - map creation
      - generation latency
      - retrieval status
      - judge score

3. The observed prediction comes ONLY from the architecture-local
   structured field:
      decision == "ANSWER" | "ABSTAIN"

4. Invalid/missing decisions are NOT silently converted to ANSWER.
   They are excluded from the TP/FP/TN/FN confusion matrix and reported
   through invalid_decision_count and decision_coverage.

5. Technical execution failures do not automatically invalidate a valid
   semantic decision. For example, ANSWER + SYNTAX_ERROR is still an ANSWER
   for OOD classification, although the execution failure is recorded
   separately. This prevents execution quality from contaminating OOD metrics.

6. Metrics are reported:
      - per generator model × architecture
      - pooled micro summary per architecture
      - macro mean/std across generator models per architecture

7. Positive class = OOD / ABSTAIN.

Confusion matrix
----------------
TP = expected ABSTAIN, actual ABSTAIN
FN = expected ABSTAIN, actual ANSWER
FP = expected ANSWER,  actual ABSTAIN
TN = expected ANSWER,  actual ANSWER

Outputs
-------
ood_metrics_detailed.csv
ood_metrics_micro_summary.csv
ood_metrics_macro_summary.csv
ood_metrics_records.csv
ood_metrics_summary.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


OOD_METRICS_VERSION = "hydrographrag_ood_metrics_v2_freeze"

DEFAULT_RESULTS_PATH = "generation_results.json"
DEFAULT_GROUND_TRUTH_PATH = "ground_truth.json"
DEFAULT_OUTPUT_DIR = "."

VALID_DECISIONS = {"ANSWER", "ABSTAIN"}

# Frozen primary benchmark architectures.
# Main benchmark cache is OFF for all modes. Therefore the old duplicate
# HydroGraphRAG_no_Cache primary mode is intentionally absent.
PRIMARY_ARCHITECTURES = [
    "Baseline",
    "VectorRAG",
    "HydroGraphRAG",
    "HydroGraphRAG_no_CDA",
    "HydroGraphRAG_no_WKT",
    "HydroGraphRAG_no_Template",
    "HydroGraphRAG_no_OOD",
    "HydroGraphRAG_no_OntologyRetrieval",
    "HydroGraphRAG_no_Sandbox",
]

EXPECTED_CATEGORY_COUNTS = {
    "explicit": 60,
    "semi-explicit": 67,
    "implicit": 83,
    "anomalous": 75,
}

VALID_CATEGORIES = set(
    EXPECTED_CATEGORY_COUNTS
)


# ============================================================
# BASIC UTILITIES
# ============================================================

def normalize_text(value: Any) -> str:
    return " ".join(
        str(value or "").strip().split()
    )


def normalize_decision(value: Any) -> str:
    text = normalize_text(
        value
    ).upper()

    # Exact structured values are preferred.
    if text == "ANSWER":
        return "ANSWER"

    if text == "ABSTAIN":
        return "ABSTAIN"

    # Conservative compatibility with values such as "DECISION: ANSWER".
    if "ABSTAIN" in text:
        return "ABSTAIN"

    if "ANSWER" in text:
        return "ANSWER"

    return "INVALID"


def safe_div(
    numerator: float,
    denominator: float,
) -> Optional[float]:
    if denominator == 0:
        return None

    return numerator / denominator


def safe_mean(
    values: Sequence[float],
) -> Optional[float]:
    clean = [
        float(v)
        for v in values
        if v is not None
        and not math.isnan(
            float(v)
        )
    ]

    if not clean:
        return None

    return sum(clean) / len(clean)


def safe_stdev(
    values: Sequence[float],
) -> Optional[float]:
    clean = [
        float(v)
        for v in values
        if v is not None
        and not math.isnan(
            float(v)
        )
    ]

    if not clean:
        return None

    if len(clean) == 1:
        return 0.0

    return statistics.stdev(
        clean
    )


def round_or_none(
    value: Optional[float],
    digits: int = 6,
) -> Optional[float]:
    if value is None:
        return None

    return round(
        float(value),
        digits,
    )


def sha256_file(
    path: Path,
) -> str:
    h = hashlib.sha256()

    with path.open(
        "rb"
    ) as f:
        while True:
            chunk = f.read(
                1024 * 1024
            )

            if not chunk:
                break

            h.update(
                chunk
            )

    return h.hexdigest()


def sha256_text_normalized(
    path: Path,
) -> str:
    """
    Canonical SHA-256 independent of CRLF/LF line endings.
    """
    raw = path.read_bytes()
    raw = raw.replace(
        b"\r\n",
        b"\n",
    ).replace(
        b"\r",
        b"\n",
    )

    return hashlib.sha256(
        raw
    ).hexdigest()


def write_json(
    path: Path,
    payload: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )


def write_csv(
    path: Path,
    rows: Sequence[Dict[str, Any]],
    fieldnames: Sequence[str],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(
                fieldnames
            ),
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                row
            )


# ============================================================
# FROZEN GROUND TRUTH
# ============================================================

def load_ground_truth(
    path: Path,
    strict_frozen_counts: bool = True,
) -> Tuple[
    List[Dict[str, Any]],
    Dict[str, Dict[str, Any]],
]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(
            f
        )

    if not isinstance(
        data,
        list,
    ):
        raise ValueError(
            "ground_truth.json must contain a JSON list."
        )

    by_id: Dict[
        str,
        Dict[str, Any],
    ] = {}

    categories = Counter()

    for item in data:
        if not isinstance(
            item,
            dict,
        ):
            raise ValueError(
                "Every ground-truth item must be an object."
            )

        query_id = normalize_text(
            item.get(
                "id"
            )
        )

        if not query_id:
            raise ValueError(
                "Ground-truth item missing id."
            )

        if query_id in by_id:
            raise ValueError(
                f"Duplicate ground-truth id: {query_id}"
            )

        category = normalize_text(
            item.get(
                "category"
            )
        ).lower()

        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category for query {query_id}: {category!r}"
            )

        expected_decision = normalize_decision(
            item.get(
                "expected_decision"
            )
        )

        if expected_decision not in VALID_DECISIONS:
            raise ValueError(
                "Ground-truth expected_decision must be ANSWER/ABSTAIN "
                f"for query {query_id}; got {expected_decision!r}"
            )

        # Frozen semantic invariant.
        if (
            category == "anomalous"
            and expected_decision
            != "ABSTAIN"
        ):
            raise ValueError(
                "Frozen GT inconsistency: anomalous query "
                f"{query_id} must expect ABSTAIN."
            )

        if (
            category != "anomalous"
            and expected_decision
            != "ANSWER"
        ):
            raise ValueError(
                "Frozen GT inconsistency: valid query "
                f"{query_id} must expect ANSWER."
            )

        categories[
            category
        ] += 1

        by_id[
            query_id
        ] = item

    if strict_frozen_counts:
        if len(
            data
        ) != 285:
            raise ValueError(
                "Frozen benchmark size mismatch: "
                f"expected=285 actual={len(data)}"
            )

        actual_counts = {
            category: categories.get(
                category,
                0,
            )
            for category in sorted(
                VALID_CATEGORIES
            )
        }

        expected_counts = {
            category: EXPECTED_CATEGORY_COUNTS[
                category
            ]
            for category in sorted(
                VALID_CATEGORIES
            )
        }

        if (
            actual_counts
            != expected_counts
        ):
            raise ValueError(
                "Frozen category counts mismatch: "
                f"expected={expected_counts} "
                f"actual={actual_counts}"
            )

    return data, by_id


# ============================================================
# GENERATION RESULTS
# ============================================================

def load_generation_results(
    path: Path,
) -> List[Dict[str, Any]]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(
            f
        )

    if not isinstance(
        data,
        list,
    ):
        raise ValueError(
            "generation_results.json must contain a JSON list."
        )

    for index, item in enumerate(
        data
    ):
        if not isinstance(
            item,
            dict,
        ):
            raise ValueError(
                "Every generation model block must be an object; "
                f"index={index}"
            )

        if not normalize_text(
            item.get(
                "model"
            )
        ):
            raise ValueError(
                f"Generation model block #{index} missing model."
            )

        metrics = item.get(
            "metrics"
        )

        if not isinstance(
            metrics,
            list,
        ):
            raise ValueError(
                f"Model {item.get('model')} has non-list metrics."
            )

    return data


def is_execution_failure(
    failure_type: Any,
) -> bool:
    """
    Record technical failure information without changing OOD prediction.

    A valid ANSWER/ABSTAIN decision remains usable for OOD classification.
    """
    normalized = normalize_text(
        failure_type
    ).upper()

    return (
        bool(
            normalized
        )
        and normalized
        not in {
            "NONE",
            "NULL",
            "OK",
            "SUCCESS",
        }
    )


def build_prediction_records(
    generation_data: Sequence[
        Dict[str, Any]
    ],
    gt_by_id: Dict[
        str,
        Dict[str, Any]
    ],
    strict_architectures: bool = True,
) -> List[Dict[str, Any]]:
    records: List[
        Dict[str, Any]
    ] = []

    seen_keys = set()

    for model_block in generation_data:
        model = normalize_text(
            model_block.get(
                "model"
            )
        ) or "unknown_model"

        metrics = model_block.get(
            "metrics",
            [],
        )

        for query_block in metrics:
            if not isinstance(
                query_block,
                dict,
            ):
                raise ValueError(
                    f"Invalid metric entry for model {model}."
                )

            query_id = normalize_text(
                query_block.get(
                    "query_id",
                    query_block.get(
                        "id"
                    ),
                )
            )

            if not query_id:
                raise ValueError(
                    f"Metric entry missing query_id for model {model}."
                )

            if query_id not in gt_by_id:
                raise ValueError(
                    "Generation result contains query absent from frozen GT: "
                    f"model={model} query_id={query_id}"
                )

            gold = gt_by_id[
                query_id
            ]

            category = normalize_text(
                gold.get(
                    "category"
                )
            ).lower()

            expected_decision = normalize_decision(
                gold.get(
                    "expected_decision"
                )
            )

            if strict_architectures:
                present = [
                    arch
                    for arch in PRIMARY_ARCHITECTURES
                    if arch in query_block
                ]

                # Partial/smoke generation files are allowed, but unknown
                # architecture names are rejected if they look like result blocks.
                known_non_arch_fields = {
                    "query_id",
                    "id",
                    "query",
                    "category",
                    "expected_entities",
                }

                unknown_arch_like = [
                    key
                    for key, value
                    in query_block.items()
                    if key not in known_non_arch_fields
                    and key not in PRIMARY_ARCHITECTURES
                    and isinstance(
                        value,
                        dict,
                    )
                    and (
                        "decision" in value
                        or "failure_type" in value
                    )
                ]

                if unknown_arch_like:
                    raise ValueError(
                        "Unknown architecture result block(s): "
                        + ", ".join(
                            sorted(
                                unknown_arch_like
                            )
                        )
                    )

            for architecture in PRIMARY_ARCHITECTURES:
                if architecture not in query_block:
                    continue

                result = query_block[
                    architecture
                ]

                if not isinstance(
                    result,
                    dict,
                ):
                    raise ValueError(
                        "Architecture result must be an object: "
                        f"model={model} arch={architecture} query={query_id}"
                    )

                key = (
                    model,
                    architecture,
                    query_id,
                )

                if key in seen_keys:
                    raise ValueError(
                        "Duplicate model/architecture/query record: "
                        f"{key}"
                    )

                seen_keys.add(
                    key
                )

                actual_decision = normalize_decision(
                    result.get(
                        "decision"
                    )
                )

                decision_valid_field = result.get(
                    "decision_valid"
                )

                if decision_valid_field is None:
                    decision_valid = (
                        actual_decision
                        in VALID_DECISIONS
                    )
                else:
                    decision_valid = (
                        bool(
                            decision_valid_field
                        )
                        and actual_decision
                        in VALID_DECISIONS
                    )

                failure_type = normalize_text(
                    result.get(
                        "failure_type",
                        "NONE",
                    )
                ).upper() or "NONE"

                technical_failure = is_execution_failure(
                    failure_type
                )

                is_ood = (
                    expected_decision
                    == "ABSTAIN"
                )

                predicted_ood: Optional[
                    bool
                ]

                confusion_label: Optional[
                    str
                ]

                if not decision_valid:
                    predicted_ood = None
                    confusion_label = None

                else:
                    predicted_ood = (
                        actual_decision
                        == "ABSTAIN"
                    )

                    if (
                        is_ood
                        and predicted_ood
                    ):
                        confusion_label = "TP"

                    elif (
                        is_ood
                        and not predicted_ood
                    ):
                        confusion_label = "FN"

                    elif (
                        not is_ood
                        and predicted_ood
                    ):
                        confusion_label = "FP"

                    else:
                        confusion_label = "TN"

                records.append({
                    "Model": model,
                    "Architecture": (
                        architecture
                    ),
                    "Query_ID": query_id,
                    "Category": category,
                    "Expected_Decision": (
                        expected_decision
                    ),
                    "Actual_Decision": (
                        actual_decision
                    ),
                    "Decision_Valid": (
                        decision_valid
                    ),
                    "OOD_Ground_Truth": (
                        is_ood
                    ),
                    "Predicted_OOD": (
                        predicted_ood
                    ),
                    "Confusion_Label": (
                        confusion_label
                    ),
                    "Failure_Type": (
                        failure_type
                    ),
                    "Technical_Failure": (
                        technical_failure
                    ),
                    "Generation_Error": (
                        normalize_text(
                            result.get(
                                "generation_error"
                            )
                        )
                    ),
                    "Abstain_Reason": (
                        normalize_text(
                            result.get(
                                "abstain_reason"
                            )
                        )
                    ),
                })

    if not records:
        raise RuntimeError(
            "No architecture-level generation records found."
        )

    return records


# ============================================================
# METRICS
# ============================================================

def summarize_records(
    records: Sequence[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:
    n_total = len(
        records
    )

    eligible = [
        r
        for r in records
        if bool(
            r.get(
                "Decision_Valid"
            )
        )
    ]

    invalid = [
        r
        for r in records
        if not bool(
            r.get(
                "Decision_Valid"
            )
        )
    ]

    technical_failures = [
        r
        for r in records
        if bool(
            r.get(
                "Technical_Failure"
            )
        )
    ]

    counts = Counter(
        r.get(
            "Confusion_Label"
        )
        for r in eligible
        if r.get(
            "Confusion_Label"
        )
    )

    tp = int(
        counts.get(
            "TP",
            0,
        )
    )
    fp = int(
        counts.get(
            "FP",
            0,
        )
    )
    tn = int(
        counts.get(
            "TN",
            0,
        )
    )
    fn = int(
        counts.get(
            "FN",
            0,
        )
    )

    n_eligible = (
        tp + fp + tn + fn
    )

    expected_ood = (
        tp + fn
    )

    expected_valid = (
        tn + fp
    )

    predicted_ood = (
        tp + fp
    )

    predicted_answer = (
        tn + fn
    )

    precision = safe_div(
        tp,
        tp + fp,
    )

    recall = safe_div(
        tp,
        tp + fn,
    )

    if (
        precision is None
        or recall is None
    ):
        f1 = None

    elif (
        precision + recall
        == 0
    ):
        f1 = 0.0

    else:
        f1 = (
            2
            * precision
            * recall
            / (
                precision
                + recall
            )
        )

    specificity = safe_div(
        tn,
        tn + fp,
    )

    frr = safe_div(
        fp,
        fp + tn,
    )

    # In this benchmark, false acceptance means accepting an OOD query
    # by producing ANSWER instead of ABSTAIN.
    far = safe_div(
        fn,
        fn + tp,
    )

    accuracy = safe_div(
        tp + tn,
        n_eligible,
    )

    balanced_accuracy: Optional[
        float
    ]

    if (
        recall is None
        or specificity is None
    ):
        balanced_accuracy = None
    else:
        balanced_accuracy = (
            recall
            + specificity
        ) / 2.0

    coverage = safe_div(
        n_eligible,
        n_total,
    )

    invalid_rate = safe_div(
        len(
            invalid
        ),
        n_total,
    )

    technical_failure_rate = (
        safe_div(
            len(
                technical_failures
            ),
            n_total,
        )
    )

    return {
        "N_Total": n_total,
        "N_Eligible": n_eligible,
        "N_Invalid_Decision": len(
            invalid
        ),
        "N_Technical_Failure": len(
            technical_failures
        ),
        "Expected_OOD": expected_ood,
        "Expected_Valid": expected_valid,
        "Predicted_OOD": predicted_ood,
        "Predicted_Answer": predicted_answer,
        "TP": tp,
        "FP": fp,
        "TN": tn,
        "FN": fn,
        "OOD_Precision": (
            round_or_none(
                precision
            )
        ),
        "OOD_Recall": (
            round_or_none(
                recall
            )
        ),
        "OOD_F1": (
            round_or_none(
                f1
            )
        ),
        "False_Rejection_Rate": (
            round_or_none(
                frr
            )
        ),
        "False_Acceptance_Rate": (
            round_or_none(
                far
            )
        ),
        "Specificity": (
            round_or_none(
                specificity
            )
        ),
        "Accuracy": (
            round_or_none(
                accuracy
            )
        ),
        "Balanced_Accuracy": (
            round_or_none(
                balanced_accuracy
            )
        ),
        "Decision_Coverage": (
            round_or_none(
                coverage
            )
        ),
        "Invalid_Decision_Rate": (
            round_or_none(
                invalid_rate
            )
        ),
        "Technical_Failure_Rate": (
            round_or_none(
                technical_failure_rate
            )
        ),
    }


def detailed_by_model_architecture(
    records: Sequence[
        Dict[str, Any]
    ],
) -> List[Dict[str, Any]]:
    groups: Dict[
        Tuple[str, str],
        List[
            Dict[str, Any]
        ],
    ] = defaultdict(
        list
    )

    for record in records:
        groups[
            (
                record[
                    "Model"
                ],
                record[
                    "Architecture"
                ],
            )
        ].append(
            record
        )

    rows = []

    for (
        model,
        architecture,
    ), group in sorted(
        groups.items()
    ):
        row = {
            "Model": model,
            "Architecture": (
                architecture
            ),
        }

        row.update(
            summarize_records(
                group
            )
        )

        rows.append(
            row
        )

    return rows


def micro_by_architecture(
    records: Sequence[
        Dict[str, Any]
    ],
) -> List[Dict[str, Any]]:
    groups: Dict[
        str,
        List[
            Dict[str, Any]
        ],
    ] = defaultdict(
        list
    )

    for record in records:
        groups[
            record[
                "Architecture"
            ]
        ].append(
            record
        )

    rows = []

    for architecture in PRIMARY_ARCHITECTURES:
        group = groups.get(
            architecture
        )

        if not group:
            continue

        row = {
            "Architecture": architecture,
        }

        row.update(
            summarize_records(
                group
            )
        )

        rows.append(
            row
        )

    return rows


def macro_by_architecture(
    detailed_rows: Sequence[
        Dict[str, Any]
    ],
) -> List[Dict[str, Any]]:
    groups: Dict[
        str,
        List[
            Dict[str, Any]
        ],
    ] = defaultdict(
        list
    )

    for row in detailed_rows:
        groups[
            row[
                "Architecture"
            ]
        ].append(
            row
        )

    metric_names = [
        "OOD_Precision",
        "OOD_Recall",
        "OOD_F1",
        "False_Rejection_Rate",
        "False_Acceptance_Rate",
        "Specificity",
        "Accuracy",
        "Balanced_Accuracy",
        "Decision_Coverage",
        "Invalid_Decision_Rate",
        "Technical_Failure_Rate",
    ]

    rows = []

    for architecture in PRIMARY_ARCHITECTURES:
        group = groups.get(
            architecture
        )

        if not group:
            continue

        row: Dict[
            str,
            Any,
        ] = {
            "Architecture": (
                architecture
            ),
            "N_Models": len(
                group
            ),
        }

        for metric_name in metric_names:
            values = [
                item.get(
                    metric_name
                )
                for item in group
                if item.get(
                    metric_name
                )
                is not None
            ]

            row[
                f"{metric_name}_Mean"
            ] = round_or_none(
                safe_mean(
                    values
                )
            )

            row[
                f"{metric_name}_Std"
            ] = round_or_none(
                safe_stdev(
                    values
                )
            )

        rows.append(
            row
        )

    return rows


# ============================================================
# PREFLIGHT
# ============================================================

def validate_generation_coverage(
    records: Sequence[
        Dict[str, Any]
    ],
    expected_models: Optional[int] = None,
    require_complete: bool = False,
) -> Dict[str, Any]:
    models = sorted({
        str(
            r[
                "Model"
            ]
        )
        for r in records
    })

    architectures = sorted({
        str(
            r[
                "Architecture"
            ]
        )
        for r in records
    })

    counts = Counter(
        (
            r[
                "Model"
            ],
            r[
                "Architecture"
            ],
        )
        for r in records
    )

    incomplete = []

    for model in models:
        for architecture in architectures:
            n = counts.get(
                (
                    model,
                    architecture,
                ),
                0,
            )

            if (
                require_complete
                and n != 285
            ):
                incomplete.append({
                    "model": model,
                    "architecture": (
                        architecture
                    ),
                    "records": n,
                    "expected": 285,
                })

    if (
        expected_models is not None
        and len(
            models
        ) != expected_models
    ):
        raise ValueError(
            "Generator model count mismatch: "
            f"expected={expected_models} actual={len(models)} "
            f"models={models}"
        )

    if (
        require_complete
        and set(
            architectures
        )
        != set(
            PRIMARY_ARCHITECTURES
        )
    ):
        raise ValueError(
            "Architecture set mismatch for complete run: "
            f"expected={PRIMARY_ARCHITECTURES} "
            f"actual={architectures}"
        )

    if incomplete:
        raise ValueError(
            "Incomplete model×architecture result coverage: "
            + json.dumps(
                incomplete[:20],
                ensure_ascii=False,
            )
        )

    return {
        "models": models,
        "architectures": (
            architectures
        ),
        "record_count": len(
            records
        ),
    }


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Compute HydroGraphRAG OOD metrics from "
            "structured ANSWER/ABSTAIN decisions."
        )
    )

    parser.add_argument(
        "--results",
        default=DEFAULT_RESULTS_PATH,
        help=(
            "Path to generation_results.json."
        ),
    )

    parser.add_argument(
        "--ground-truth",
        default=DEFAULT_GROUND_TRUTH_PATH,
        help=(
            "Path to frozen ground_truth.json."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Directory for OOD CSV/JSON artifacts."
        ),
    )

    parser.add_argument(
        "--expected-models",
        type=int,
        default=None,
        help=(
            "Optional expected generator model count. "
            "Use 7 for the final complete benchmark."
        ),
    )

    parser.add_argument(
        "--require-complete",
        action="store_true",
        help=(
            "Require 285 records for every model × architecture "
            "and the exact frozen architecture set."
        ),
    )

    parser.add_argument(
        "--allow-nonfrozen-gt-counts",
        action="store_true",
        help=(
            "Disable the strict 285 / 60-67-83-75 frozen count check. "
            "Intended only for unit/smoke tests."
        ),
    )

    args = parser.parse_args()

    results_path = Path(
        args.results
    ).resolve()

    gt_path = Path(
        args.ground_truth
    ).resolve()

    output_dir = Path(
        args.output_dir
    ).resolve()

    if not results_path.is_file():
        raise FileNotFoundError(
            results_path
        )

    if not gt_path.is_file():
        raise FileNotFoundError(
            gt_path
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    ground_truth, gt_by_id = (
        load_ground_truth(
            gt_path,
            strict_frozen_counts=(
                not args.allow_nonfrozen_gt_counts
            ),
        )
    )

    generation_data = (
        load_generation_results(
            results_path
        )
    )

    records = (
        build_prediction_records(
            generation_data,
            gt_by_id,
            strict_architectures=True,
        )
    )

    coverage = (
        validate_generation_coverage(
            records,
            expected_models=(
                args.expected_models
            ),
            require_complete=(
                args.require_complete
            ),
        )
    )

    detailed = (
        detailed_by_model_architecture(
            records
        )
    )

    micro = (
        micro_by_architecture(
            records
        )
    )

    macro = (
        macro_by_architecture(
            detailed
        )
    )

    # --------------------------------------------------------
    # WRITE RECORD-LEVEL AUDIT
    # --------------------------------------------------------

    record_fields = [
        "Model",
        "Architecture",
        "Query_ID",
        "Category",
        "Expected_Decision",
        "Actual_Decision",
        "Decision_Valid",
        "OOD_Ground_Truth",
        "Predicted_OOD",
        "Confusion_Label",
        "Failure_Type",
        "Technical_Failure",
        "Generation_Error",
        "Abstain_Reason",
    ]

    write_csv(
        output_dir
        / "ood_metrics_records.csv",
        records,
        record_fields,
    )

    detailed_fields = [
        "Model",
        "Architecture",
        "N_Total",
        "N_Eligible",
        "N_Invalid_Decision",
        "N_Technical_Failure",
        "Expected_OOD",
        "Expected_Valid",
        "Predicted_OOD",
        "Predicted_Answer",
        "TP",
        "FP",
        "TN",
        "FN",
        "OOD_Precision",
        "OOD_Recall",
        "OOD_F1",
        "False_Rejection_Rate",
        "False_Acceptance_Rate",
        "Specificity",
        "Accuracy",
        "Balanced_Accuracy",
        "Decision_Coverage",
        "Invalid_Decision_Rate",
        "Technical_Failure_Rate",
    ]

    write_csv(
        output_dir
        / "ood_metrics_detailed.csv",
        detailed,
        detailed_fields,
    )

    micro_fields = [
        "Architecture",
        *[
            field
            for field in detailed_fields
            if field
            not in {
                "Model",
                "Architecture",
            }
        ],
    ]

    write_csv(
        output_dir
        / "ood_metrics_micro_summary.csv",
        micro,
        micro_fields,
    )

    macro_fields = [
        "Architecture",
        "N_Models",
    ]

    macro_metric_names = [
        "OOD_Precision",
        "OOD_Recall",
        "OOD_F1",
        "False_Rejection_Rate",
        "False_Acceptance_Rate",
        "Specificity",
        "Accuracy",
        "Balanced_Accuracy",
        "Decision_Coverage",
        "Invalid_Decision_Rate",
        "Technical_Failure_Rate",
    ]

    for metric_name in macro_metric_names:
        macro_fields.extend([
            f"{metric_name}_Mean",
            f"{metric_name}_Std",
        ])

    write_csv(
        output_dir
        / "ood_metrics_macro_summary.csv",
        macro,
        macro_fields,
    )

    summary_json = {
        "ood_metrics_version": (
            OOD_METRICS_VERSION
        ),
        "policy": {
            "positive_class": (
                "OOD/ABSTAIN"
            ),
            "ground_truth_source": (
                "frozen expected_decision"
            ),
            "prediction_source": (
                "architecture-local decision only"
            ),
            "execution_status_used_as_prediction": (
                False
            ),
            "invalid_decision_defaulted_to_answer": (
                False
            ),
            "invalid_decisions_excluded_from_confusion_matrix": (
                True
            ),
            "valid_decision_kept_even_if_execution_failed": (
                True
            ),
        },
        "ground_truth": {
            "path": str(
                gt_path
            ),
            "sha256_normalized_lf": (
                sha256_text_normalized(
                    gt_path
                )
            ),
            "sha256_raw": (
                sha256_file(
                    gt_path
                )
            ),
            "N": len(
                ground_truth
            ),
            "category_counts": dict(
                Counter(
                    normalize_text(
                        item.get(
                            "category"
                        )
                    ).lower()
                    for item in ground_truth
                )
            ),
        },
        "generation_results": {
            "path": str(
                results_path
            ),
            "sha256_raw": (
                sha256_file(
                    results_path
                )
            ),
        },
        "coverage": coverage,
        "architectures": (
            PRIMARY_ARCHITECTURES
        ),
        "micro_by_architecture": (
            micro
        ),
        "macro_by_architecture": (
            macro
        ),
    }

    write_json(
        output_dir
        / "ood_metrics_summary.json",
        summary_json,
    )

    print("=" * 80)
    print("HydroGraphRAG OOD Metrics FINAL")
    print("=" * 80)
    print(
        "Ground truth SHA256 (normalized LF): "
        + summary_json[
            "ground_truth"
        ][
            "sha256_normalized_lf"
        ]
    )
    print(
        "Records: "
        f"{len(records)}"
    )
    print(
        "Models: "
        + ", ".join(
            coverage[
                "models"
            ]
        )
    )
    print(
        "Architectures: "
        + ", ".join(
            coverage[
                "architectures"
            ]
        )
    )
    print("")

    print(
        "MICRO SUMMARY BY ARCHITECTURE"
    )

    for row in micro:
        print(
            (
                f"{row['Architecture']}: "
                f"TP={row['TP']} "
                f"FP={row['FP']} "
                f"TN={row['TN']} "
                f"FN={row['FN']} | "
                f"P={row['OOD_Precision']} "
                f"R={row['OOD_Recall']} "
                f"F1={row['OOD_F1']} "
                f"FRR={row['False_Rejection_Rate']} "
                f"FAR={row['False_Acceptance_Rate']} "
                f"Coverage={row['Decision_Coverage']}"
            )
        )

    print("")
    print("Saved:")
    print(
        "  ood_metrics_records.csv"
    )
    print(
        "  ood_metrics_detailed.csv"
    )
    print(
        "  ood_metrics_micro_summary.csv"
    )
    print(
        "  ood_metrics_macro_summary.csv"
    )
    print(
        "  ood_metrics_summary.json"
    )


if __name__ == "__main__":
    main()
