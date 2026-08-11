#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HydroGraphRAG final evaluation pipeline.

Stages
------
1. PRE-FLIGHT
   - validate frozen ground_truth.json
   - verify SHA256 against benchmark_manifest.json
   - validate category counts and ANSWER/ABSTAIN policy
   - snapshot hashes of active evaluation code
   - NEVER rebuild or mutate the gold benchmark

2. GENERATION
   - execute the active evaluation/run_generation.py
   - preserve its own generation artifacts and manifest

3. JUDGE INPUT STAGING
   - read generation artifacts:
       results/<model>/<mode>/<id>/metadata.json
   - flatten metadata["result"] into judge-compatible per-query JSON
   - write them into a separate judge_inputs/ directory
   - never modify original generation outputs

4. JUDGE
   - execute the active evaluation/run_judge.py
   - use frozen ground_truth.json and staged judge inputs

5. PIPELINE MANIFEST
   - save exact hashes, commands, statuses, timestamps and paths

IMPORTANT
---------
This script deliberately DOES NOT call build_gold_candidates_v*.py.
Benchmark construction happens offline before the freeze boundary.

No human evaluation is implemented here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ============================================================
# CONFIG
# ============================================================

PIPELINE_VERSION = "hydrographrag_final_pipeline_v1"

EXPECTED_DATASET_SIZE = 285

EXPECTED_CATEGORY_COUNTS = {
    "explicit": 60,
    "semi-explicit": 67,
    "implicit": 83,
    "anomalous": 75,
}

DEFAULT_GROUND_TRUTH = "ground_truth.json"
DEFAULT_BENCHMARK_MANIFEST = "benchmark_manifest.json"

DEFAULT_GENERATION_SCRIPT = "run_generation.py"
DEFAULT_JUDGE_SCRIPT = "run_judge.py"

DEFAULT_RESULTS_DIR = "results"
DEFAULT_JUDGE_INPUTS_DIR = "judge_inputs"
DEFAULT_JUDGE_OUTPUT_DIR = "judge_results"
DEFAULT_PIPELINE_RUNS_DIR = "pipeline_runs"

VALID_STAGES = {
    "preflight",
    "generation",
    "stage-judge-inputs",
    "judge",
    "all",
}


# ============================================================
# BASIC HELPERS
# ============================================================

def now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )
def sha256_text_normalized(path: Path) -> str:
    raw = path.read_bytes()
    raw = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def run_id_now() -> str:
    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def normalize_category(value: Any) -> str:
    return (
        normalize_text(value)
        .lower()
        .replace("_", "-")
    )


def normalize_decision(value: Any) -> str:
    text = normalize_text(
        value
    ).upper()

    if "ABSTAIN" in text:
        return "ABSTAIN"

    if "ANSWER" in text:
        return "ANSWER"

    return "INVALID"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open(
        "rb",
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


def load_json(
    path: Path,
) -> Any:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(
            f
        )


def ensure_file(
    path: Path,
    label: str,
) -> None:
    if not path.is_file():
        raise FileNotFoundError(
            f"{label} not found: {path}"
        )


def ensure_dir(
    path: Path,
) -> None:
    path.mkdir(
        parents=True,
        exist_ok=True,
    )


def relative_or_absolute(
    path: Path,
    root: Path,
) -> str:
    try:
        return str(
            path.relative_to(
                root
            )
        )
    except Exception:
        return str(
            path
        )


# ============================================================
# BENCHMARK FREEZE VALIDATION
# ============================================================

def validate_ground_truth(
    ground_truth_path: Path,
    benchmark_manifest_path: Optional[Path],
) -> Dict[str, Any]:
    dataset = load_json(
        ground_truth_path
    )

    if not isinstance(
        dataset,
        list,
    ):
        raise ValueError(
            "ground_truth.json must contain a JSON list."
        )

    errors: List[str] = []
    warnings: List[str] = []

    ids = []
    categories = Counter()

    answer_count = 0
    abstain_count = 0

    unresolved_entities = 0
    unmatched_wkt = 0

    for index, item in enumerate(
        dataset,
        start=1,
    ):
        if not isinstance(
            item,
            dict,
        ):
            errors.append(
                f"Item #{index} is not an object."
            )
            continue

        query_id = normalize_text(
            item.get(
                "id"
            )
        )

        if not query_id:
            errors.append(
                f"Item #{index} has no id."
            )
        else:
            ids.append(
                query_id
            )

        query = normalize_text(
            item.get(
                "query"
            )
        )

        if not query:
            errors.append(
                f"ID={query_id}: missing query."
            )

        category = normalize_category(
            item.get(
                "category"
            )
        )

        categories[
            category
        ] += 1

        expected_decision = (
            normalize_decision(
                item.get(
                    "expected_decision"
                )
            )
        )

        if expected_decision == "ANSWER":
            answer_count += 1

        elif expected_decision == "ABSTAIN":
            abstain_count += 1

        else:
            errors.append(
                (
                    f"ID={query_id}: invalid "
                    f"expected_decision="
                    f"{item.get('expected_decision')!r}"
                )
            )

        should_abstain = (
            category
            == "anomalous"
        )

        correct_expected = (
            "ABSTAIN"
            if should_abstain
            else "ANSWER"
        )

        if (
            expected_decision
            != correct_expected
        ):
            errors.append(
                (
                    f"ID={query_id}: category={category} "
                    f"requires {correct_expected}, "
                    f"found {expected_decision}."
                )
            )

        review = item.get(
            "gold_review",
            {}
        )

        if isinstance(
            review,
            dict,
        ):
            unresolved_entities += len(
                review.get(
                    "unresolved_entities",
                    [],
                )
                or []
            )

            unmatched_wkt += len(
                review.get(
                    "unmatched_expected_wkt",
                    [],
                )
                or []
            )

    duplicates = [
        query_id
        for (
            query_id,
            count,
        ) in Counter(
            ids
        ).items()
        if count > 1
    ]

    if duplicates:
        errors.append(
            (
                "Duplicate IDs: "
                + ", ".join(
                    duplicates[:20]
                )
            )
        )

    if len(
        dataset
    ) != EXPECTED_DATASET_SIZE:
        errors.append(
            (
                f"Expected {EXPECTED_DATASET_SIZE} "
                f"queries, found {len(dataset)}."
            )
        )

    for (
        category,
        expected_count,
    ) in (
        EXPECTED_CATEGORY_COUNTS.items()
    ):
        actual = categories.get(
            category,
            0,
        )

        if actual != expected_count:
            errors.append(
                (
                    f"Category {category}: "
                    f"expected {expected_count}, "
                    f"found {actual}."
                )
            )

    if unresolved_entities:
        errors.append(
            (
                "Frozen benchmark contains "
                f"{unresolved_entities} unresolved "
                "entity entries."
            )
        )

    if unmatched_wkt:
        errors.append(
            (
                "Frozen benchmark contains "
                f"{unmatched_wkt} unmatched expected WKT entries."
            )
        )

    gt_sha256 = sha256_text_normalized(
    ground_truth_path
)

    manifest_payload = None
    manifest_expected_sha = None
    manifest_sha_match = None

    if (
        benchmark_manifest_path
        is not None
        and benchmark_manifest_path.is_file()
    ):
        manifest_payload = load_json(
            benchmark_manifest_path
        )

        if not isinstance(
            manifest_payload,
            dict,
        ):
            errors.append(
                "benchmark_manifest.json is not an object."
            )

        else:
            manifest_expected_sha = normalize_text(
                manifest_payload.get(
                    "compact_ground_truth_sha256"
                )
                or manifest_payload.get(
                    "ground_truth_sha256"
                )
                or manifest_payload.get(
                    "benchmark_sha256"
                )
            )

            if manifest_expected_sha:
                manifest_sha_match = (
                    manifest_expected_sha
                    == gt_sha256
                )

                if not manifest_sha_match:
                    errors.append(
                        (
                            "Frozen GT SHA256 does not match "
                            "benchmark manifest. "
                            f"GT={gt_sha256}, "
                            f"manifest={manifest_expected_sha}"
                        )
                    )

            else:
                warnings.append(
                    "Benchmark manifest does not contain a GT SHA256 field."
                )

            manifest_size = manifest_payload.get(
                "dataset_size"
            )

            if (
                manifest_size is not None
                and int(
                    manifest_size
                ) != len(
                    dataset
                )
            ):
                errors.append(
                    (
                        "Benchmark manifest dataset_size "
                        f"{manifest_size} != {len(dataset)}."
                    )
                )

    else:
        warnings.append(
            "benchmark_manifest.json not found; SHA cross-check skipped."
        )

    report = {
        "valid": not errors,
        "ground_truth_path": str(
            ground_truth_path
        ),
        "ground_truth_sha256": (
            gt_sha256
        ),
        "dataset_size": len(
            dataset
        ),
        "category_counts": dict(
            categories
        ),
        "answer_count": (
            answer_count
        ),
        "abstain_count": (
            abstain_count
        ),
        "unresolved_entities": (
            unresolved_entities
        ),
        "unmatched_expected_wkt": (
            unmatched_wkt
        ),
        "manifest_path": (
            str(
                benchmark_manifest_path
            )
            if benchmark_manifest_path
            else None
        ),
        "manifest_expected_sha256": (
            manifest_expected_sha
        ),
        "manifest_sha_match": (
            manifest_sha_match
        ),
        "errors": errors,
        "warnings": warnings,
    }

    if errors:
        raise RuntimeError(
            "Frozen benchmark validation failed:\n- "
            + "\n- ".join(
                errors
            )
        )

    return report


# ============================================================
# CODE SNAPSHOT / FREEZE HASHES
# ============================================================

def collect_code_hashes(
    evaluation_dir: Path,
    project_root: Path,
    generation_script: Path,
    judge_script: Path,
) -> Dict[str, Any]:
    candidates = {
        "run_generation.py": (
            generation_script
        ),
        "run_judge.py": (
            judge_script
        ),
        "planner/generator.py": (
            project_root
            / "planner"
            / "generator.py"
        ),
    }

    result = {}

    for name, path in candidates.items():
        if path.is_file():
            result[name] = {
                "path": str(
                    path
                ),
                "sha256": sha256_file(
                    path
                ),
                "size_bytes": path.stat().st_size,
            }

        else:
            result[name] = {
                "path": str(
                    path
                ),
                "missing": True,
            }

    return result


# ============================================================
# SUBPROCESS
# ============================================================

def run_command(
    *,
    command: Sequence[str],
    cwd: Path,
    log_path: Path,
    env: Optional[
        Dict[str, str]
    ] = None,
) -> Dict[str, Any]:
    ensure_dir(
        log_path.parent
    )

    started_at = now_iso()
    started = time.perf_counter()

    merged_env = os.environ.copy()

    if env:
        merged_env.update(
            env
        )

    with log_path.open(
        "w",
        encoding="utf-8",
    ) as log_file:
        log_file.write(
            "$ "
            + " ".join(
                command
            )
            + "\n\n"
        )

        log_file.flush()

        process = subprocess.Popen(
            list(
                command
            ),
            cwd=str(
                cwd
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=merged_env,
            bufsize=1,
        )

        assert (
            process.stdout
            is not None
        )

        for line in (
            process.stdout
        ):
            sys.stdout.write(
                line
            )

            log_file.write(
                line
            )

        returncode = (
            process.wait()
        )

    elapsed = (
        time.perf_counter()
        - started
    )

    return {
        "command": list(
            command
        ),
        "cwd": str(
            cwd
        ),
        "started_at": (
            started_at
        ),
        "finished_at": (
            now_iso()
        ),
        "elapsed_s": elapsed,
        "returncode": (
            returncode
        ),
        "success": (
            returncode
            == 0
        ),
        "log_path": str(
            log_path
        ),
    }


# ============================================================
# GENERATION → JUDGE INPUT STAGING
# ============================================================

def find_generation_metadata_files(
    results_dir: Path,
) -> List[Path]:
    return sorted(
        results_dir.rglob(
            "metadata.json"
        )
    )


def flatten_generation_metadata(
    *,
    metadata_path: Path,
    ground_truth_by_id: Dict[
        str,
        Dict[str, Any]
    ],
) -> Dict[str, Any]:
    payload = load_json(
        metadata_path
    )

    if not isinstance(
        payload,
        dict,
    ):
        raise ValueError(
            (
                "Generation metadata is not "
                f"an object: {metadata_path}"
            )
        )

    result = payload.get(
        "result"
    )

    if not isinstance(
        result,
        dict,
    ):
        raise ValueError(
            (
                "Generation metadata missing "
                f"result object: {metadata_path}"
            )
        )

    query_id = normalize_text(
        payload.get(
            "query_id"
        )
        or result.get(
            "query_id"
        )
        or result.get(
            "id"
        )
    )

    if not query_id:
        raise ValueError(
            (
                "Generation metadata has no "
                f"query id: {metadata_path}"
            )
        )

    gold = ground_truth_by_id.get(
        query_id
    )

    if gold is None:
        raise KeyError(
            (
                f"No frozen gold for query id "
                f"{query_id}."
            )
        )

    model = normalize_text(
        payload.get(
            "model"
        )
        or result.get(
            "model"
        )
        or "unknown_model"
    )

    mode = normalize_text(
        payload.get(
            "architecture"
        )
        or result.get(
            "architecture"
        )
        or result.get(
            "mode"
        )
        or "unknown_mode"
    )

    raw_response = normalize_text(
        result.get(
            "raw_response"
        )
        or result.get(
            "response"
        )
        or result.get(
            "generated_response"
        )
    )

    code = normalize_text(
        result.get(
            "code_extracted"
        )
        or result.get(
            "code"
        )
    )

    flattened = {
        "id": (
            int(query_id)
            if query_id.isdigit()
            else query_id
        ),
        "query_id": query_id,
        "query": gold.get(
            "query",
            ""
        ),
        "category": gold.get(
            "category",
            ""
        ),
        "model": model,
        "mode": mode,
        "architecture": mode,

        # Generated decision/output.
        "decision": result.get(
            "decision"
        ),
        "raw_response": raw_response,
        "code": code,

        # Technical state.
        "failure_type": (
            result.get(
                "failure_type"
            )
        ),
        "generation_error": (
            result.get(
                "generation_error"
            )
        ),
        "execution_status": (
            result.get(
                "execution_status"
            )
        ),
        "syntax": result.get(
            "syntax"
        ),
        "exec": result.get(
            "exec"
        ),
        "has_map": result.get(
            "has_map"
        ),

        # Retrieval evidence.
        "retrieved_entities": (
            result.get(
                "retrieved_entities",
                []
            )
        ),
        "retrieved_triples": (
            result.get(
                "retrieved_triples",
                []
            )
        ),
        "retrieval_context": (
            result.get(
                "retrieval_context",
                []
            )
        ),

        # Provenance only.
        "source_generation_metadata": (
            str(
                metadata_path
            )
        ),
        "run_id": payload.get(
            "run_id"
        ),
        "generation_prompt_sha256": (
            result.get(
                "prompt_sha256"
            )
            or result.get(
                "prompt_hash"
            )
        ),
        "artifact_dir": result.get(
            "artifact_dir"
        ),
    }

    return flattened


def load_gt_by_id(
    ground_truth_path: Path,
) -> Dict[str, Dict[str, Any]]:
    dataset = load_json(
        ground_truth_path
    )

    return {
        normalize_text(
            item.get(
                "id"
            )
        ): item
        for item in dataset
        if isinstance(
            item,
            dict,
        )
    }


def prepare_judge_inputs(
    *,
    results_dir: Path,
    judge_inputs_dir: Path,
    ground_truth_path: Path,
    clean: bool,
) -> Dict[str, Any]:
    if clean and (
        judge_inputs_dir.exists()
    ):
        shutil.rmtree(
            judge_inputs_dir
        )

    ensure_dir(
        judge_inputs_dir
    )

    gt_by_id = load_gt_by_id(
        ground_truth_path
    )

    metadata_files = (
        find_generation_metadata_files(
            results_dir
        )
    )

    if not metadata_files:
        raise RuntimeError(
            (
                "No generation metadata.json files "
                f"found below {results_dir}."
            )
        )

    staged = 0
    errors = []

    models = Counter()
    modes = Counter()
    ids = Counter()

    for metadata_path in (
        metadata_files
    ):
        try:
            flattened = (
                flatten_generation_metadata(
                    metadata_path=(
                        metadata_path
                    ),
                    ground_truth_by_id=(
                        gt_by_id
                    ),
                )
            )

            model = normalize_text(
                flattened.get(
                    "model"
                )
            )

            mode = normalize_text(
                flattened.get(
                    "mode"
                )
            )

            query_id = normalize_text(
                flattened.get(
                    "query_id"
                )
            )

            safe_model = (
                sanitize_path_component(
                    model
                )
            )

            safe_mode = (
                sanitize_path_component(
                    mode
                )
            )

            target = (
                judge_inputs_dir
                / safe_model
                / safe_mode
                / f"{query_id}.json"
            )

            write_json(
                target,
                flattened,
            )

            staged += 1

            models[
                model
            ] += 1

            modes[
                mode
            ] += 1

            ids[
                query_id
            ] += 1

        except Exception as exc:
            errors.append({
                "metadata_path": (
                    str(
                        metadata_path
                    )
                ),
                "error": (
                    f"{type(exc).__name__}: "
                    f"{exc}"
                ),
            })

    report = {
        "metadata_files_found": (
            len(
                metadata_files
            )
        ),
        "staged_files": (
            staged
        ),
        "errors_count": (
            len(
                errors
            )
        ),
        "errors": errors,
        "models": dict(
            models
        ),
        "modes": dict(
            modes
        ),
        "unique_query_ids": (
            len(
                ids
            )
        ),
        "judge_inputs_dir": (
            str(
                judge_inputs_dir
            )
        ),
    }

    write_json(
        judge_inputs_dir
        / "_staging_manifest.json",
        report,
    )

    if errors:
        raise RuntimeError(
            (
                f"Judge staging produced "
                f"{len(errors)} error(s). "
                "See _staging_manifest.json."
            )
        )

    return report


def sanitize_path_component(
    value: str,
) -> str:
    import re

    clean = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        value.strip(),
    )

    return (
        clean[:160]
        or "unknown"
    )


# ============================================================
# PIPELINE RUN MANIFEST
# ============================================================

class PipelineManifest:

    def __init__(
        self,
        path: Path,
        run_id: str,
    ):
        self.path = path

        self.data: Dict[
            str,
            Any,
        ] = {
            "pipeline_version": (
                PIPELINE_VERSION
            ),
            "run_id": run_id,
            "created_at": now_iso(),
            "status": (
                "INITIALIZING"
            ),
            "stages": {},
        }

        self.flush()

    def flush(
        self,
    ) -> None:
        write_json(
            self.path,
            self.data,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.data[
            key
        ] = value

        self.flush()

    def stage(
        self,
        name: str,
        payload: Dict[
            str,
            Any,
        ],
    ) -> None:
        self.data[
            "stages"
        ][name] = payload

        self.flush()


# ============================================================
# CLI
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen HydroGraphRAG "
            "evaluation pipeline."
        )
    )

    parser.add_argument(
        "--stage",
        choices=sorted(
            VALID_STAGES
        ),
        default="all",
        help=(
            "Pipeline stage to run."
        ),
    )

    parser.add_argument(
        "--evaluation-dir",
        default=".",
        help=(
            "Directory containing "
            "run_generation.py, run_judge.py "
            "and ground_truth.json."
        ),
    )

    parser.add_argument(
        "--ground-truth",
        default=DEFAULT_GROUND_TRUTH,
    )

    parser.add_argument(
        "--benchmark-manifest",
        default=(
            DEFAULT_BENCHMARK_MANIFEST
        ),
    )

    parser.add_argument(
        "--generation-script",
        default=(
            DEFAULT_GENERATION_SCRIPT
        ),
    )

    parser.add_argument(
        "--judge-script",
        default=(
            DEFAULT_JUDGE_SCRIPT
        ),
    )

    parser.add_argument(
        "--results-dir",
        default=(
            DEFAULT_RESULTS_DIR
        ),
    )

    parser.add_argument(
        "--judge-inputs-dir",
        default=(
            DEFAULT_JUDGE_INPUTS_DIR
        ),
    )

    parser.add_argument(
        "--judge-output-dir",
        default=(
            DEFAULT_JUDGE_OUTPUT_DIR
        ),
    )

    parser.add_argument(
        "--pipeline-runs-dir",
        default=(
            DEFAULT_PIPELINE_RUNS_DIR
        ),
    )

    parser.add_argument(
        "--run-id",
        default=None,
    )

    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help=(
            "For --stage all, use existing "
            "generation artifacts."
        ),
    )

    parser.add_argument(
        "--clean-judge-inputs",
        action="store_true",
        help=(
            "Remove and rebuild the judge "
            "staging directory."
        ),
    )

    parser.add_argument(
        "--clean-judge-results",
        action="store_true",
        help=(
            "Remove judge_results before judging."
        ),
    )

    parser.add_argument(
        "--judge-ids",
        nargs="*",
        default=None,
        help=(
            "Optional query IDs passed to "
            "run_judge.py for smoke testing."
        ),
    )

    parser.add_argument(
        "--judge-model",
        default=None,
        help=(
            "Optional override passed to "
            "run_judge.py."
        ),
    )

    parser.add_argument(
        "--judge-overwrite",
        action="store_true",
    )

    args = parser.parse_args()

    evaluation_dir = Path(
        args.evaluation_dir
    ).resolve()

    project_root = (
        evaluation_dir.parent
        if evaluation_dir.name
        == "evaluation"
        else evaluation_dir.parent
    )

    ground_truth_path = (
        evaluation_dir
        / args.ground_truth
    ).resolve()

    benchmark_manifest_path = (
        evaluation_dir
        / args.benchmark_manifest
    ).resolve()

    generation_script = (
        evaluation_dir
        / args.generation_script
    ).resolve()

    judge_script = (
        evaluation_dir
        / args.judge_script
    ).resolve()

    results_dir = (
        evaluation_dir
        / args.results_dir
    ).resolve()

    judge_inputs_dir = (
        evaluation_dir
        / args.judge_inputs_dir
    ).resolve()

    judge_output_dir = (
        evaluation_dir
        / args.judge_output_dir
    ).resolve()

    pipeline_runs_dir = (
        evaluation_dir
        / args.pipeline_runs_dir
    ).resolve()

    run_id = (
        args.run_id
        or run_id_now()
    )

    run_dir = (
        pipeline_runs_dir
        / run_id
    )

    ensure_dir(
        run_dir
    )

    manifest = PipelineManifest(
        run_dir
        / "pipeline_manifest.json",
        run_id,
    )

    manifest.set(
        "status",
        "PREFLIGHT",
    )

    # --------------------------------------------------------
    # Guardrail: active evaluation must never rebuild gold.
    # --------------------------------------------------------

    forbidden_builder_names = [
        "build_gold_candidates",
        "ground_truth_compact_v",
    ]

    own_name = Path(
        __file__
    ).name.lower()

    if any(
        marker in own_name
        for marker in forbidden_builder_names
    ):
        raise RuntimeError(
            "Pipeline must not be a gold-builder script."
        )

    # --------------------------------------------------------
    # PRE-FLIGHT
    # --------------------------------------------------------

    ensure_file(
        ground_truth_path,
        "Frozen ground truth",
    )

    ensure_file(
        generation_script,
        "Generation script",
    )

    ensure_file(
        judge_script,
        "Judge script",
    )

    benchmark_report = (
        validate_ground_truth(
            ground_truth_path=(
                ground_truth_path
            ),
            benchmark_manifest_path=(
                benchmark_manifest_path
                if benchmark_manifest_path.is_file()
                else None
            ),
        )
    )

    code_hashes = collect_code_hashes(
        evaluation_dir=(
            evaluation_dir
        ),
        project_root=(
            project_root
        ),
        generation_script=(
            generation_script
        ),
        judge_script=(
            judge_script
        ),
    )

    freeze_snapshot = {
        "created_at": now_iso(),
        "run_id": run_id,
        "ground_truth": {
            "path": str(
                ground_truth_path
            ),
            "sha256": sha256_file(
                ground_truth_path
            ),
        },
        "benchmark_manifest": {
            "path": str(
                benchmark_manifest_path
            ),
            "sha256": (
                sha256_file(
                    benchmark_manifest_path
                )
                if benchmark_manifest_path.is_file()
                else None
            ),
        },
        "code": code_hashes,
        "policy": {
            "gold_is_read_only": True,
            "gold_builder_called": False,
            "generation_receives_gold_answers": False,
            "judge_receives_frozen_gold": True,
            "human_evaluation": False,
        },
    }

    write_json(
        run_dir
        / "frozen_hashes.json",
        freeze_snapshot,
    )

    manifest.stage(
        "preflight",
        {
            "success": True,
            "benchmark": (
                benchmark_report
            ),
            "freeze_snapshot": (
                freeze_snapshot
            ),
        },
    )

    print("=" * 72)
    print("HydroGraphRAG Final Evaluation Pipeline")
    print("=" * 72)
    print(
        f"Run ID: {run_id}"
    )
    print(
        f"Evaluation dir: {evaluation_dir}"
    )
    print(
        "Frozen GT SHA256: "
        + benchmark_report[
            "ground_truth_sha256"
        ]
    )
    print(
        "Dataset: "
        f"{benchmark_report['dataset_size']}"
    )
    print(
        "Categories: "
        f"{benchmark_report['category_counts']}"
    )
    print("Preflight: OK")
    print("")

    if args.stage == "preflight":
        manifest.set(
            "status",
            "COMPLETE",
        )
        print(
            "Preflight-only run complete."
        )
        return

    # --------------------------------------------------------
    # GENERATION
    # --------------------------------------------------------

    should_run_generation = (
        args.stage
        in {
            "generation",
            "all",
        }
        and not args.skip_generation
    )

    if should_run_generation:
        manifest.set(
            "status",
            "GENERATION",
        )

        generation_log = (
            run_dir
            / "generation.log"
        )

        generation_command = [
            sys.executable,
            str(
                generation_script
            ),
        ]

        generation_result = (
            run_command(
                command=(
                    generation_command
                ),
                cwd=evaluation_dir,
                log_path=(
                    generation_log
                ),
            )
        )

        manifest.stage(
            "generation",
            generation_result,
        )

        if not generation_result[
            "success"
        ]:
            manifest.set(
                "status",
                "FAILED_GENERATION",
            )

            raise RuntimeError(
                (
                    "Generation stage failed. "
                    f"See {generation_log}"
                )
            )

    elif (
        args.stage
        in {
            "generation",
        }
        and args.skip_generation
    ):
        raise RuntimeError(
            (
                "--skip-generation cannot be "
                "used with --stage generation."
            )
        )

    if args.stage == "generation":
        manifest.set(
            "status",
            "COMPLETE",
        )

        print(
            "Generation-only run complete."
        )
        return

    # --------------------------------------------------------
    # JUDGE INPUT STAGING
    # --------------------------------------------------------

    if args.stage in {
        "stage-judge-inputs",
        "judge",
        "all",
    }:
        manifest.set(
            "status",
            "STAGING_JUDGE_INPUTS",
        )

        if not results_dir.is_dir():
            manifest.set(
                "status",
                "FAILED_STAGING",
            )

            raise FileNotFoundError(
                (
                    "Generation results directory "
                    f"not found: {results_dir}"
                )
            )

        staging_report = (
            prepare_judge_inputs(
                results_dir=(
                    results_dir
                ),
                judge_inputs_dir=(
                    judge_inputs_dir
                ),
                ground_truth_path=(
                    ground_truth_path
                ),
                clean=(
                    args.clean_judge_inputs
                ),
            )
        )

        manifest.stage(
            "judge_input_staging",
            {
                "success": True,
                **staging_report,
            },
        )

        print(
            "Judge input staging: "
            f"{staging_report['staged_files']} files"
        )

    if (
        args.stage
        == "stage-judge-inputs"
    ):
        manifest.set(
            "status",
            "COMPLETE",
        )

        print(
            "Judge-input staging complete."
        )
        return

    # --------------------------------------------------------
    # JUDGE
    # --------------------------------------------------------

    if args.stage in {
        "judge",
        "all",
    }:
        manifest.set(
            "status",
            "JUDGE",
        )

        if (
            args.clean_judge_results
            and judge_output_dir.exists()
        ):
            shutil.rmtree(
                judge_output_dir
            )

        ensure_dir(
            judge_output_dir
        )

        judge_command = [
            sys.executable,
            str(
                judge_script
            ),
            "--ground-truth",
            str(
                ground_truth_path
            ),
            "--results-root",
            str(
                judge_inputs_dir
            ),
            "--output-root",
            str(
                judge_output_dir
            ),
        ]

        if args.judge_ids:
            judge_command.append(
                "--ids"
            )

            judge_command.extend(
                [
                    str(v)
                    for v in args.judge_ids
                ]
            )

        if args.judge_model:
            judge_command.extend([
                "--judge-model",
                args.judge_model,
            ])

        if args.judge_overwrite:
            judge_command.append(
                "--overwrite"
            )

        judge_log = (
            run_dir
            / "judge.log"
        )

        judge_result = run_command(
            command=judge_command,
            cwd=evaluation_dir,
            log_path=judge_log,
        )

        manifest.stage(
            "judge",
            judge_result,
        )

        if not judge_result[
            "success"
        ]:
            manifest.set(
                "status",
                "FAILED_JUDGE",
            )

            raise RuntimeError(
                (
                    "Judge stage failed. "
                    f"See {judge_log}"
                )
            )

    # --------------------------------------------------------
    # FINAL SNAPSHOT
    # --------------------------------------------------------

    outputs = {
        "generation_results_dir": (
            str(
                results_dir
            )
        ),
        "judge_inputs_dir": (
            str(
                judge_inputs_dir
            )
        ),
        "judge_output_dir": (
            str(
                judge_output_dir
            )
        ),
        "judge_manifest": (
            str(
                judge_output_dir
                / "judge_manifest.json"
            )
        ),
        "judge_results_json": (
            str(
                judge_output_dir
                / "judge_results.json"
            )
        ),
        "judge_results_csv": (
            str(
                judge_output_dir
                / "judge_results.csv"
            )
        ),
        "judge_summary": (
            str(
                judge_output_dir
                / "judge_summary.json"
            )
        ),
    }

    manifest.set(
        "outputs",
        outputs,
    )

    manifest.set(
        "finished_at",
        now_iso(),
    )

    manifest.set(
        "status",
        "COMPLETE",
    )

    print("")
    print("=" * 72)
    print("PIPELINE COMPLETE")
    print("=" * 72)
    print(
        "Pipeline manifest: "
        + str(
            manifest.path
        )
    )
    print(
        "Frozen hashes:     "
        + str(
            run_dir
            / "frozen_hashes.json"
        )
    )
    print(
        "Judge inputs:      "
        + str(
            judge_inputs_dir
        )
    )
    print(
        "Judge results:     "
        + str(
            judge_output_dir
        )
    )


if __name__ == "__main__":
    main()
