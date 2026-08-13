#!/usr/bin/env python3
"""
Prepare safe non-overlapping query-ID splits for the remaining Wave-2 work.

Purpose
-------
This script is READ-ONLY with respect to benchmark generation outputs.
It never deletes, moves, edits, or rewrites anything inside parallel_runs/.

It:
  1. loads the frozen ground_truth.json;
  2. verifies the expected 285-query benchmark;
  3. checks, for each target model, which query IDs are fully complete
     across all 9 frozen architectures;
  4. treats a query as COMPLETE only when every architecture has both
     metadata.json and response.txt and metadata matches model/architecture/query_id;
  5. computes REMAINING = frozen query IDs - fully complete query IDs;
  6. distributes remaining IDs round-robin into:
       codestral      -> 2 parts
       mistral-nemo   -> 2 parts
       gemma4:31b     -> 4 parts
  7. writes plain-text query-ID files plus a JSON manifest and CSV audit.

IMPORTANT
---------
If the current Wave-2 job is still running, the output is only a snapshot.
Before launching split workers:
  - stop the old Wave-2 job in a controlled way;
  - rerun this script once more;
  - use ONLY the freshly generated split files from that final snapshot.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


# ============================================================
# FROZEN BENCHMARK CONFIGURATION
# ============================================================

EVAL_DIR = Path(__file__).resolve().parent

GROUND_TRUTH = EVAL_DIR / "ground_truth.json"
PARALLEL_RUNS = EVAL_DIR / "parallel_runs"

EXPECTED_QUERY_COUNT = 285

ARCHITECTURES = [
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

EXPECTED_ARCHITECTURE_COUNT = 9

MODEL_CONFIG = {
    "codestral": {
        "model_name": "codestral",
        "results_root": (
            PARALLEL_RUNS
            / "codestral"
            / "results"
            / "codestral"
        ),
        "parts": 2,
        "split_prefix": "codestral",
    },
    "mistral-nemo": {
        "model_name": "mistral-nemo",
        "results_root": (
            PARALLEL_RUNS
            / "mistral-nemo"
            / "results"
            / "mistral-nemo"
        ),
        "parts": 2,
        "split_prefix": "mistral_nemo",
    },
    "gemma4:31b": {
        "model_name": "gemma4:31b",
        "results_root": (
            PARALLEL_RUNS
            / "gemma4_31b"
            / "results"
            / "gemma4_31b"
        ),
        "parts": 4,
        "split_prefix": "gemma4",
    },
}


# ============================================================
# HELPERS
# ============================================================

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_text(path: Path, text: str) -> None:
    """
    Atomic write for newly generated split/audit files.
    Does not touch generation outputs.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )

    tmp_path = Path(tmp_name)

    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

        os.replace(tmp_path, path)

    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def atomic_write_json(path: Path, payload: Any) -> None:
    atomic_write_text(
        path,
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        + "\n",
    )


def query_sort_key(value: str) -> Tuple[int, Any]:
    value = str(value).strip()

    if value.isdigit():
        return (0, int(value))

    return (1, value)


def load_ground_truth() -> Tuple[List[dict], List[str], Dict[str, dict]]:
    if not GROUND_TRUTH.is_file():
        raise FileNotFoundError(
            f"Frozen ground truth not found: {GROUND_TRUTH}"
        )

    with GROUND_TRUTH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise RuntimeError(
            "ground_truth.json must contain a JSON list."
        )

    if len(data) != EXPECTED_QUERY_COUNT:
        raise RuntimeError(
            "Frozen benchmark query count mismatch: "
            f"expected={EXPECTED_QUERY_COUNT}, actual={len(data)}"
        )

    ordered_ids: List[str] = []
    by_id: Dict[str, dict] = {}

    for index, row in enumerate(data, start=1):
        if not isinstance(row, dict):
            raise RuntimeError(
                f"Ground-truth row #{index} is not a dict."
            )

        query_id = str(row.get("id", "")).strip()

        if not query_id:
            raise RuntimeError(
                f"Ground-truth row #{index} has no query ID."
            )

        if query_id in by_id:
            raise RuntimeError(
                f"Duplicate ground-truth query ID: {query_id}"
            )

        ordered_ids.append(query_id)
        by_id[query_id] = row

    return data, ordered_ids, by_id


def verify_frozen_design() -> None:
    if len(ARCHITECTURES) != EXPECTED_ARCHITECTURE_COUNT:
        raise RuntimeError(
            "Architecture count mismatch: "
            f"expected={EXPECTED_ARCHITECTURE_COUNT}, "
            f"actual={len(ARCHITECTURES)}"
        )

    if len(set(ARCHITECTURES)) != len(ARCHITECTURES):
        raise RuntimeError(
            "Duplicate architecture names in frozen configuration."
        )

    expected_parts = {
        "codestral": 2,
        "mistral-nemo": 2,
        "gemma4:31b": 4,
    }

    actual_parts = {
        model: int(config["parts"])
        for model, config in MODEL_CONFIG.items()
    }

    if actual_parts != expected_parts:
        raise RuntimeError(
            "Unexpected split design: "
            f"{actual_parts!r}"
        )


def validate_metadata(
    metadata_path: Path,
    expected_model: str,
    expected_architecture: str,
    expected_query_id: str,
) -> Tuple[bool, str]:
    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as exc:
        return (
            False,
            f"metadata unreadable: {type(exc).__name__}: {exc}",
        )

    if not isinstance(metadata, dict):
        return False, "metadata is not a JSON object"

    actual_model = str(metadata.get("model", "")).strip()
    actual_architecture = str(
        metadata.get("architecture", "")
    ).strip()
    actual_query_id = str(
        metadata.get("query_id", "")
    ).strip()

    if actual_model != expected_model:
        return (
            False,
            "model mismatch: "
            f"expected={expected_model!r}, actual={actual_model!r}",
        )

    if actual_architecture != expected_architecture:
        return (
            False,
            "architecture mismatch: "
            f"expected={expected_architecture!r}, "
            f"actual={actual_architecture!r}",
        )

    if actual_query_id != expected_query_id:
        return (
            False,
            "query_id mismatch: "
            f"expected={expected_query_id!r}, "
            f"actual={actual_query_id!r}",
        )

    return True, ""


def inspect_query(
    results_root: Path,
    model_name: str,
    query_id: str,
) -> Tuple[bool, List[dict]]:
    """
    A query is fully complete only if all 9 architectures have:
      - response.txt
      - metadata.json
      - metadata matching model, architecture, query_id
    """
    problems: List[dict] = []

    for architecture in ARCHITECTURES:
        artifact_dir = (
            results_root
            / architecture
            / query_id
        )

        response_path = (
            artifact_dir
            / "response.txt"
        )

        metadata_path = (
            artifact_dir
            / "metadata.json"
        )

        if not response_path.is_file():
            problems.append(
                {
                    "architecture": architecture,
                    "problem": "missing response.txt",
                    "path": str(response_path),
                }
            )

        if not metadata_path.is_file():
            problems.append(
                {
                    "architecture": architecture,
                    "problem": "missing metadata.json",
                    "path": str(metadata_path),
                }
            )
            continue

        ok, reason = validate_metadata(
            metadata_path=metadata_path,
            expected_model=model_name,
            expected_architecture=architecture,
            expected_query_id=query_id,
        )

        if not ok:
            problems.append(
                {
                    "architecture": architecture,
                    "problem": reason,
                    "path": str(metadata_path),
                }
            )

    return len(problems) == 0, problems


def inspect_model(
    model_name: str,
    results_root: Path,
    ordered_query_ids: List[str],
) -> Dict[str, Any]:
    complete_ids: List[str] = []
    remaining_ids: List[str] = []
    partial_details: Dict[str, List[dict]] = {}

    for query_id in ordered_query_ids:
        complete, problems = inspect_query(
            results_root=results_root,
            model_name=model_name,
            query_id=query_id,
        )

        if complete:
            complete_ids.append(query_id)
        else:
            remaining_ids.append(query_id)

            # Store audit detail only for queries where something exists
            # or metadata is inconsistent. Completely untouched future
            # queries would otherwise create a huge noisy report.
            any_existing = any(
                (
                    results_root
                    / architecture
                    / query_id
                ).exists()
                for architecture in ARCHITECTURES
            )

            if any_existing:
                partial_details[query_id] = problems

    return {
        "complete_ids": complete_ids,
        "remaining_ids": remaining_ids,
        "partial_details": partial_details,
    }


def round_robin_split(
    ordered_ids: List[str],
    part_count: int,
) -> List[List[str]]:
    if part_count <= 0:
        raise ValueError("part_count must be positive")

    parts: List[List[str]] = [
        []
        for _ in range(part_count)
    ]

    for index, query_id in enumerate(ordered_ids):
        parts[index % part_count].append(query_id)

    return parts


def category_counts(
    ids: Iterable[str],
    gt_by_id: Dict[str, dict],
) -> Dict[str, int]:
    counter: Counter[str] = Counter()

    for query_id in ids:
        row = gt_by_id[query_id]
        category = str(
            row.get("category", "")
        ).strip().lower() or "unknown"
        counter[category] += 1

    return dict(
        sorted(counter.items())
    )


def ensure_no_split_overlap(
    parts: List[List[str]],
    expected_ids: List[str],
) -> None:
    flattened = [
        query_id
        for part in parts
        for query_id in part
    ]

    if len(flattened) != len(set(flattened)):
        counts = Counter(flattened)
        duplicates = sorted(
            [
                query_id
                for query_id, count in counts.items()
                if count > 1
            ],
            key=query_sort_key,
        )

        raise RuntimeError(
            "Split overlap detected. Duplicate IDs: "
            + ", ".join(duplicates)
        )

    if set(flattened) != set(expected_ids):
        missing = sorted(
            set(expected_ids) - set(flattened),
            key=query_sort_key,
        )

        extra = sorted(
            set(flattened) - set(expected_ids),
            key=query_sort_key,
        )

        raise RuntimeError(
            "Split coverage mismatch. "
            f"missing={missing}, extra={extra}"
        )


def write_csv_audit(
    path: Path,
    rows: List[dict],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "model",
        "query_id",
        "category",
        "status",
        "assigned_part",
    ]

    fd, tmp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )

    tmp_path = Path(tmp_name)

    try:
        with os.fdopen(
            fd,
            "w",
            encoding="utf-8-sig",
            newline="",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(rows)

        os.replace(
            tmp_path,
            path,
        )

    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare non-overlapping query-ID split files "
            "for unfinished Wave-2 models."
        )
    )

    parser.add_argument(
        "--output-dir",
        default=str(EVAL_DIR / "splits"),
        help=(
            "Directory for generated split files and audits. "
            "Default: evaluation/splits"
        ),
    )

    parser.add_argument(
        "--tag",
        default=None,
        help=(
            "Optional snapshot tag used only in the manifest metadata."
        ),
    )

    args = parser.parse_args()

    output_dir = Path(
        args.output_dir
    ).resolve()

    verify_frozen_design()

    (
        ground_truth,
        ordered_query_ids,
        gt_by_id,
    ) = load_ground_truth()

    print()
    print("=" * 72)
    print("HydroGraphRAG Wave-2 Split Preparer")
    print("=" * 72)
    print(f"Ground truth:      {GROUND_TRUTH}")
    print(f"Queries:           {len(ordered_query_ids)}")
    print(f"Architectures:     {len(ARCHITECTURES)}")
    print(f"Parallel runs:     {PARALLEL_RUNS}")
    print(f"Output directory:  {output_dir}")
    print()
    print(
        "READ-ONLY GUARANTEE: generation outputs are inspected only; "
        "nothing under parallel_runs/ is modified."
    )
    print()

    manifest: Dict[str, Any] = {
        "created_at_utc": utc_now_iso(),
        "snapshot_tag": args.tag,
        "ground_truth_path": str(GROUND_TRUTH),
        "expected_query_count": EXPECTED_QUERY_COUNT,
        "architecture_count": len(ARCHITECTURES),
        "architectures": ARCHITECTURES,
        "model_splits": {},
        "warning": (
            "If Wave-2 was still running when this file was created, "
            "rerun prepare_split.py after stopping the old Wave-2 job "
            "and use the new split snapshot."
        ),
    }

    audit_rows: List[dict] = []

    for model_key, config in MODEL_CONFIG.items():
        model_name = str(
            config["model_name"]
        )

        results_root = Path(
            config["results_root"]
        )

        part_count = int(
            config["parts"]
        )

        split_prefix = str(
            config["split_prefix"]
        )

        print("-" * 72)
        print(f"MODEL: {model_name}")
        print(f"Results root: {results_root}")
        print(f"Target parts: {part_count}")

        inspection = inspect_model(
            model_name=model_name,
            results_root=results_root,
            ordered_query_ids=ordered_query_ids,
        )

        complete_ids = inspection[
            "complete_ids"
        ]

        remaining_ids = inspection[
            "remaining_ids"
        ]

        partial_details = inspection[
            "partial_details"
        ]

        parts = round_robin_split(
            remaining_ids,
            part_count,
        )

        ensure_no_split_overlap(
            parts=parts,
            expected_ids=remaining_ids,
        )

        print(
            f"Complete queries:  {len(complete_ids)}/{EXPECTED_QUERY_COUNT}"
        )
        print(
            f"Remaining queries: {len(remaining_ids)}/{EXPECTED_QUERY_COUNT}"
        )
        print(
            f"Partial/in-progress queries detected: "
            f"{len(partial_details)}"
        )

        assigned_part_by_id: Dict[str, str] = {}

        part_manifest: List[dict] = []

        for part_index, part_ids in enumerate(
            parts,
            start=1,
        ):
            filename = (
                f"{split_prefix}_part{part_index}.txt"
            )

            path = (
                output_dir
                / filename
            )

            text = "".join(
                f"{query_id}\n"
                for query_id in part_ids
            )

            atomic_write_text(
                path,
                text,
            )

            assigned_name = (
                f"part{part_index}"
            )

            for query_id in part_ids:
                assigned_part_by_id[
                    query_id
                ] = assigned_name

            part_categories = category_counts(
                part_ids,
                gt_by_id,
            )

            print(
                f"  {filename:<28} "
                f"{len(part_ids):>3} queries | "
                f"{part_categories}"
            )

            part_manifest.append(
                {
                    "part": part_index,
                    "file": str(path),
                    "query_count": len(part_ids),
                    "query_ids": part_ids,
                    "category_counts": part_categories,
                }
            )

        for query_id in ordered_query_ids:
            status = (
                "COMPLETE"
                if query_id in set(complete_ids)
                else (
                    "PARTIAL_OR_IN_PROGRESS"
                    if query_id in partial_details
                    else "NOT_COMPLETE"
                )
            )

            audit_rows.append(
                {
                    "model": model_name,
                    "query_id": query_id,
                    "category": str(
                        gt_by_id[query_id].get(
                            "category",
                            "",
                        )
                    ).strip().lower(),
                    "status": status,
                    "assigned_part": (
                        assigned_part_by_id.get(
                            query_id,
                            "",
                        )
                    ),
                }
            )

        manifest["model_splits"][
            model_name
        ] = {
            "results_root": str(
                results_root
            ),
            "target_parts": part_count,
            "complete_query_count": len(
                complete_ids
            ),
            "remaining_query_count": len(
                remaining_ids
            ),
            "complete_query_ids": complete_ids,
            "remaining_query_ids": remaining_ids,
            "partial_query_count": len(
                partial_details
            ),
            "partial_details": partial_details,
            "parts": part_manifest,
        }

        print()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path = (
        output_dir
        / "split_manifest.json"
    )

    audit_path = (
        output_dir
        / "split_audit.csv"
    )

    atomic_write_json(
        manifest_path,
        manifest,
    )

    write_csv_audit(
        audit_path,
        audit_rows,
    )

    print("=" * 72)
    print("SPLIT PREPARATION COMPLETE")
    print("=" * 72)
    print(f"Manifest: {manifest_path}")
    print(f"Audit:    {audit_path}")
    print()
    print("Generated query-ID files:")

    for path in sorted(
        output_dir.glob("*.txt")
    ):
        line_count = sum(
            1
            for line in path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        )

        print(
            f"  {path.name:<28} {line_count:>3} IDs"
        )

    print()
    print("IMPORTANT:")
    print(
        "If job 21614 is still running, DO NOT launch split workers "
        "from this snapshot yet."
    )
    print(
        "After stopping the old Wave-2 job, rerun prepare_split.py "
        "and use the freshly regenerated split files."
    )
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
