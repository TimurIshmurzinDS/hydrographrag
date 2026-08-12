#!/usr/bin/env python3
"""
HydroGraphRAG final deterministic metrics aggregator.

This script DOES NOT call an LLM. It only reads frozen generation outputs,
optional judge outputs, and optional OOD outputs, then computes deterministic
aggregates for the paper.

Recommended order:
  1) finish both generation waves;
  2) freeze/check generation outputs;
  3) run ood_metrics.py on a merged generation_results.json;
  4) run run_judge.py;
  5) run this script;
  6) run export_tables.py.

The script can discover the seven per-model generation_results.json files
recursively under parallel_runs/, so no source result file is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd

ANALYSER_VERSION = "hydrographrag-analyser-v2.0"

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

VALID_CATEGORIES = {"explicit", "semi-explicit", "implicit"}
ALL_CATEGORIES = ["explicit", "semi-explicit", "implicit", "anomalous"]
EXPECTED_QUERIES_PER_MODEL = 285


def _safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _bool01(value: Any) -> int:
    return int(bool(value))


def _mean(values: Iterable[Any]) -> Optional[float]:
    xs = [x for x in (_safe_float(v) for v in values) if x is not None]
    return statistics.fmean(xs) if xs else None


def _median(values: Iterable[Any]) -> Optional[float]:
    xs = [x for x in (_safe_float(v) for v in values) if x is not None]
    return statistics.median(xs) if xs else None


def _stdev(values: Iterable[Any]) -> Optional[float]:
    xs = [x for x in (_safe_float(v) for v in values) if x is not None]
    return statistics.stdev(xs) if len(xs) >= 2 else (0.0 if len(xs) == 1 else None)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover_generation_files(root: Path) -> List[Path]:
    """Find per-model generation_results.json while avoiding derived output dirs."""
    if root.is_file():
        return [root]
    if not root.exists():
        raise FileNotFoundError(root)

    files = []
    for p in root.rglob("generation_results.json"):
        parts_lower = {part.lower() for part in p.parts}
        if "analysis_outputs" in parts_lower or "final_results" in parts_lower:
            continue
        files.append(p)
    return sorted(files)


def load_generation_blocks(files: Sequence[Path]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Load and de-duplicate model blocks. Returns blocks and source manifest rows."""
    by_model: Dict[str, Dict[str, Any]] = {}
    manifest_rows: List[Dict[str, Any]] = []

    for path in files:
        payload = _load_json(path)
        if not isinstance(payload, list):
            raise ValueError(f"{path}: generation results must be a JSON list")

        manifest_rows.append({
            "source_file": str(path.resolve()),
            "sha256": _sha256(path),
            "model_blocks": len(payload),
        })

        for block in payload:
            if not isinstance(block, dict):
                raise ValueError(f"{path}: every model block must be an object")
            model = str(block.get("model", "")).strip()
            if not model:
                raise ValueError(f"{path}: model block without model name")
            if model in by_model:
                raise ValueError(
                    f"Duplicate generator model '{model}' found in multiple generation files. "
                    "Do not silently choose one run."
                )
            metrics = block.get("metrics")
            if not isinstance(metrics, list):
                raise ValueError(f"{path}: model={model} has non-list metrics")
            by_model[model] = block

    return [by_model[m] for m in sorted(by_model)], manifest_rows


def validate_generation(blocks: Sequence[Dict[str, Any]], expected_models: Optional[int], require_complete: bool) -> Dict[str, Any]:
    models = [str(b.get("model")) for b in blocks]
    if expected_models is not None and len(models) != expected_models:
        raise ValueError(f"Expected {expected_models} models, found {len(models)}: {models}")

    duplicate_keys: List[Tuple[str, str]] = []
    missing: List[Dict[str, Any]] = []
    category_counts = Counter()
    total_records = 0

    for block in blocks:
        model = str(block["model"])
        seen_qids = set()
        metrics = block["metrics"]
        for item in metrics:
            if not isinstance(item, dict):
                raise ValueError(f"model={model}: metric item is not an object")
            qid = str(item.get("query_id", "")).strip()
            if not qid:
                raise ValueError(f"model={model}: missing query_id")
            if qid in seen_qids:
                duplicate_keys.append((model, qid))
            seen_qids.add(qid)
            category_counts[str(item.get("category", "")).strip().lower()] += 1
            for arch in PRIMARY_ARCHITECTURES:
                if arch not in item:
                    missing.append({"model": model, "query_id": qid, "architecture": arch})
                else:
                    total_records += 1

        if require_complete and len(metrics) != EXPECTED_QUERIES_PER_MODEL:
            raise ValueError(
                f"Incomplete model={model}: expected {EXPECTED_QUERIES_PER_MODEL} queries, found {len(metrics)}"
            )

        if require_complete:
            unknown_arch = set()
            for item in metrics:
                for key, value in item.items():
                    if key in {"query_id", "query", "category"}:
                        continue
                    if isinstance(value, dict) and key not in PRIMARY_ARCHITECTURES:
                        # Only flag result-like blocks.
                        if any(k in value for k in ("decision", "syntax", "exec", "total_latency")):
                            unknown_arch.add(key)
            if unknown_arch:
                raise ValueError(f"model={model}: unknown architecture blocks: {sorted(unknown_arch)}")

    if duplicate_keys:
        raise ValueError(f"Duplicate model/query keys detected: {duplicate_keys[:20]}")
    if require_complete and missing:
        raise ValueError(f"Missing architecture results: {missing[:20]}")

    if require_complete:
        expected_total = len(blocks) * EXPECTED_QUERIES_PER_MODEL * len(PRIMARY_ARCHITECTURES)
        if total_records != expected_total:
            raise ValueError(f"Expected {expected_total} architecture-query records, found {total_records}")

    return {
        "models": models,
        "model_count": len(models),
        "architecture_count": len(PRIMARY_ARCHITECTURES),
        "architecture_query_records": total_records,
        "category_counts_across_models": dict(category_counts),
        "require_complete": require_complete,
    }


def flatten_generation(blocks: Sequence[Dict[str, Any]]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for block in blocks:
        model = str(block.get("model", "unknown"))
        for item in block.get("metrics", []):
            qid = str(item.get("query_id", ""))
            category = str(item.get("category", "")).strip().lower()
            for arch in PRIMARY_ARCHITECTURES:
                payload = item.get(arch)
                if not isinstance(payload, dict):
                    continue
                retrieval = payload.get("retrieval") if isinstance(payload.get("retrieval"), dict) else {}
                rows.append({
                    "Model": model,
                    "Architecture": arch,
                    "Query_ID": qid,
                    "Category": category,
                    "Decision": payload.get("decision"),
                    "Decision_Valid": bool(payload.get("decision_valid", False)),
                    "Failure_Type": payload.get("failure_type"),
                    "Generation_Error": payload.get("generation_error"),
                    "Retrieval_Error": payload.get("retrieval_error"),
                    "Syntax_OK": _bool01(payload.get("syntax")),
                    "Exec_OK": _bool01(payload.get("exec")),
                    "Has_Map": _bool01(payload.get("has_map")),
                    "Execution_Status": payload.get("execution_status"),
                    "Execution_Timeout": _bool01(payload.get("execution_timeout")),
                    "CDA_Latency_s": _safe_float(payload.get("cda_latency")),
                    "Retrieval_Latency_s": _safe_float(payload.get("retrieval_latency")),
                    "Generation_Latency_s": _safe_float(payload.get("generation_latency")),
                    "Execution_Latency_s": _safe_float(payload.get("execution_latency")),
                    "Total_Latency_s": _safe_float(payload.get("total_latency")),
                    "Graph_Retrieval_Called": _bool01(payload.get("graph_retrieval_called")),
                    "Ontology_Retrieval_Enabled": _bool01(payload.get("ontology_retrieval_enabled")),
                    "Cache_Hit": _bool01(payload.get("cache_hit")),
                    "Retrieved_Entities_Count": len(payload.get("retrieved_entities", [])) if isinstance(payload.get("retrieved_entities"), list) else None,
                    "Retrieved_Triples_Count": _safe_float(payload.get("retrieved_triples")),
                    "Retrieval_Precision": _safe_float(retrieval.get("precision")),
                    "Retrieval_Recall": _safe_float(retrieval.get("recall")),
                    "Retrieval_F1": _safe_float(retrieval.get("f1")),
                    "Targets_Found": _safe_float(retrieval.get("targets_found")),
                    "Retrieval_Expected_Targets": _safe_float(retrieval.get("expected_targets", retrieval.get("targets_total"))),
                    "Retrieval_Retrieved_Entities": _safe_float(retrieval.get("retrieved_entities")),
                    "Retrieval_Retrieved_Triples": _safe_float(retrieval.get("retrieved_triples")),
                })
    return pd.DataFrame(rows)


def _aggregate_generation_group(group: pd.DataFrame) -> pd.Series:
    result: Dict[str, Any] = {
        "N": len(group),
        "Decision_Valid_Rate": group["Decision_Valid"].mean() if len(group) else None,
        "Syntax_OK_Rate": group["Syntax_OK"].mean() if len(group) else None,
        "Exec_Success_Rate": group["Exec_OK"].mean() if len(group) else None,
        "Map_Creation_Rate": group["Has_Map"].mean() if len(group) else None,
        "Execution_Timeout_Rate": group["Execution_Timeout"].mean() if len(group) else None,
        "Total_Latency_Mean_s": group["Total_Latency_s"].mean(),
        "Total_Latency_Median_s": group["Total_Latency_s"].median(),
        "Total_Latency_Std_s": group["Total_Latency_s"].std(ddof=1),
        "Generation_Latency_Mean_s": group["Generation_Latency_s"].mean(),
        "Retrieval_Latency_Mean_s": group["Retrieval_Latency_s"].mean(),
        "Execution_Latency_Mean_s": group["Execution_Latency_s"].mean(),
        "CDA_Latency_Mean_s": group["CDA_Latency_s"].mean(),
        "Graph_Retrieval_Called_Rate": group["Graph_Retrieval_Called"].mean(),
    }

    applicable = group[group["Retrieval_F1"].notna()]
    result.update({
        "Retrieval_N": len(applicable),
        "Entity_Precision_Mean": applicable["Retrieval_Precision"].mean() if len(applicable) else None,
        "Entity_Recall_Mean": applicable["Retrieval_Recall"].mean() if len(applicable) else None,
        "Entity_F1_Mean": applicable["Retrieval_F1"].mean() if len(applicable) else None,
        "Targets_Found_Mean": applicable["Targets_Found"].mean() if len(applicable) else None,
        "Retrieved_Entities_Mean": applicable["Retrieval_Retrieved_Entities"].mean() if len(applicable) else None,
        "Retrieved_Triples_Mean": applicable["Retrieval_Retrieved_Triples"].mean() if len(applicable) else None,
    })
    return pd.Series(result)


def aggregate_generation(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    overall = (
        df.groupby(["Model", "Architecture"], sort=True, dropna=False)
        .apply(_aggregate_generation_group)
        .reset_index()
    )
    by_category = (
        df.groupby(["Model", "Architecture", "Category"], sort=True, dropna=False)
        .apply(_aggregate_generation_group)
        .reset_index()
    )
    return overall, by_category


def load_judge_flat(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if path is None:
        return None
    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        payload = _load_json(path)
        if not isinstance(payload, list):
            raise ValueError("judge_results.json must be a list of record objects")
        rows = []
        for r in payload:
            if not isinstance(r, dict):
                continue
            scores = r.get("scores") if isinstance(r.get("scores"), dict) else {}
            subtypes = scores.get("subtypes") if isinstance(scores.get("subtypes"), dict) else {}

            def score_dim(name: str) -> Optional[float]:
                item = scores.get(name)
                return _safe_float(item.get("score")) if isinstance(item, dict) and item.get("applicable", False) else None

            def subtype(name: str, key: str) -> Any:
                item = subtypes.get(name)
                if not isinstance(item, dict):
                    return None
                if key == "score" and not item.get("applicable", False):
                    return None
                return item.get(key)

            cat = str(r.get("category", "")).strip().lower()
            rows.append({
                "query_id": str(r.get("query_id", "")),
                "category": cat,
                "generator_model": r.get("generator_model"),
                "architecture_mode": r.get("architecture_mode"),
                "judge_status": r.get("judge_status"),
                "expected_decision": r.get("expected_decision"),
                "generated_decision": r.get("generated_decision"),
                "decision_correct": (r.get("deterministic_checks") or {}).get("decision_correct") if isinstance(r.get("deterministic_checks"), dict) else None,
                "semantic_score": score_dim("semantic"),
                "structural_score": score_dim("structural"),
                "faithfulness_score": score_dim("faithfulness"),
                "faithfulness_valid_score": score_dim("faithfulness") if cat in VALID_CATEGORIES else None,
                "spatial_score": _safe_float(subtype("spatial", "score")),
                "spatial_hallucination": subtype("spatial", "hallucination"),
                "numerical_score": _safe_float(subtype("numerical", "score")),
                "numerical_hallucination": subtype("numerical", "hallucination"),
                "temporal_score": _safe_float(subtype("temporal", "score")),
                "temporal_hallucination": subtype("temporal", "hallucination"),
                "topological_score": _safe_float(subtype("topological", "score")),
                "topological_hallucination": subtype("topological", "hallucination"),
                "categorical_score": _safe_float(subtype("categorical", "score")),
                "categorical_hallucination": subtype("categorical", "hallucination"),
                "judge_latency_s": _safe_float((r.get("judge_ollama_metadata") or {}).get("latency_s")) if isinstance(r.get("judge_ollama_metadata"), dict) else None,
            })
        df = pd.DataFrame(rows)

    # Normalize column names from official run_judge.py CSV.
    required = {"query_id", "category", "generator_model", "architecture_mode", "judge_status"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Judge file missing required columns: {sorted(missing)}")
    df["query_id"] = df["query_id"].astype(str)
    df["category"] = df["category"].astype(str).str.strip().str.lower()
    return df


def _hallucination_rate(series: pd.Series) -> Optional[float]:
    if series.empty:
        return None
    values = []
    for v in series.dropna():
        if isinstance(v, str):
            t = v.strip().lower()
            if t in {"true", "1", "yes"}:
                values.append(1)
            elif t in {"false", "0", "no"}:
                values.append(0)
        else:
            values.append(int(bool(v)))
    return statistics.fmean(values) if values else None


def _aggregate_judge_group(group: pd.DataFrame) -> pd.Series:
    eligible = group[group["judge_status"] != "SKIPPED_GENERATION_FAILURE"]
    ok = eligible[eligible["judge_status"] == "OK"]
    valid = ok[ok["category"].isin(VALID_CATEGORIES)]
    out: Dict[str, Any] = {
        "Judge_N_Total": len(group),
        "Judge_N_Eligible": len(eligible),
        "Judge_N_OK": len(ok),
        "Judge_Coverage": len(ok) / len(eligible) if len(eligible) else None,
        "Semantic_Mean": ok["semantic_score"].mean() if "semantic_score" in ok else None,
        "Structural_Mean": ok["structural_score"].mean() if "structural_score" in ok else None,
        "Faithfulness_Valid_N": valid["faithfulness_valid_score"].notna().sum() if "faithfulness_valid_score" in valid else 0,
        "Faithfulness_Valid_Mean": valid["faithfulness_valid_score"].mean() if "faithfulness_valid_score" in valid else None,
        "Faithfulness_Valid_Std": valid["faithfulness_valid_score"].std(ddof=1) if "faithfulness_valid_score" in valid else None,
    }
    for dim in ["spatial", "numerical", "temporal", "topological", "categorical"]:
        score_col = f"{dim}_score"
        hall_col = f"{dim}_hallucination"
        applicable = ok[ok[score_col].notna()] if score_col in ok else ok.iloc[0:0]
        out[f"{dim.title()}_N"] = len(applicable)
        out[f"{dim.title()}_Score_Mean"] = applicable[score_col].mean() if len(applicable) else None
        out[f"{dim.title()}_Hallucination_Rate"] = _hallucination_rate(applicable[hall_col]) if len(applicable) and hall_col in applicable else None
    return pd.Series(out)


def aggregate_judge(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    overall = (
        df.groupby(["generator_model", "architecture_mode"], sort=True, dropna=False)
        .apply(_aggregate_judge_group)
        .reset_index()
        .rename(columns={"generator_model": "Model", "architecture_mode": "Architecture"})
    )
    by_category = (
        df.groupby(["generator_model", "architecture_mode", "category"], sort=True, dropna=False)
        .apply(_aggregate_judge_group)
        .reset_index()
        .rename(columns={"generator_model": "Model", "architecture_mode": "Architecture", "category": "Category"})
    )
    return overall, by_category


def load_ood_detailed(ood_dir: Optional[Path]) -> Optional[pd.DataFrame]:
    if ood_dir is None:
        return None
    path = ood_dir / "ood_metrics_detailed.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def build_ablation_delta(combined: pd.DataFrame) -> pd.DataFrame:
    """Full-minus-one deltas, always relative to full HydroGraphRAG within each model."""
    metrics_higher_better = [
        "Exec_Success_Rate", "Map_Creation_Rate", "Entity_F1_Mean",
        "Semantic_Mean", "Structural_Mean", "Faithfulness_Valid_Mean",
        "Spatial_Score_Mean", "Numerical_Score_Mean", "Temporal_Score_Mean",
        "Topological_Score_Mean", "Categorical_Score_Mean", "OOD_F1",
    ]
    metrics_lower_better = ["Total_Latency_Mean_s", "False_Rejection_Rate"]
    rows: List[Dict[str, Any]] = []

    for model, g in combined.groupby("Model"):
        full_rows = g[g["Architecture"] == "HydroGraphRAG"]
        if full_rows.empty:
            continue
        full = full_rows.iloc[0]
        for _, row in g.iterrows():
            arch = row["Architecture"]
            if arch == "HydroGraphRAG" or not str(arch).startswith("HydroGraphRAG_no_"):
                continue
            rec: Dict[str, Any] = {"Model": model, "Ablation": arch}
            for metric in metrics_higher_better:
                if metric in combined.columns:
                    a = _safe_float(full.get(metric))
                    b = _safe_float(row.get(metric))
                    rec[f"Delta_{metric}"] = (a - b) if a is not None and b is not None else None
            for metric in metrics_lower_better:
                if metric in combined.columns:
                    a = _safe_float(full.get(metric))
                    b = _safe_float(row.get(metric))
                    # positive = ablation is worse (higher) than full
                    rec[f"Delta_{metric}"] = (b - a) if a is not None and b is not None else None
            rows.append(rec)
    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Aggregate final HydroGraphRAG metrics without any AI calls.")
    p.add_argument("--generation-root", default="parallel_runs", help="Directory containing per-model generation_results.json files, or one generation_results.json file.")
    p.add_argument("--judge-results", default=None, help="Optional judge_results.csv or judge_results.json from run_judge.py.")
    p.add_argument("--ood-dir", default=None, help="Optional directory containing ood_metrics_detailed.csv from ood_metrics.py.")
    p.add_argument("--output-dir", default="analysis_outputs", help="Directory for deterministic analysis CSV/JSON outputs.")
    p.add_argument("--expected-models", type=int, default=None, help="Use 7 for the final benchmark.")
    p.add_argument("--require-complete", action="store_true", help="Require exactly 285 queries and all 9 architectures per model.")
    p.add_argument("--write-merged-generation", action="store_true", help="Also write generation_results_merged.json into output-dir. Source files are never modified.")
    args = p.parse_args()

    generation_root = Path(args.generation_root).resolve()
    outdir = Path(args.output_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    files = discover_generation_files(generation_root)
    if not files:
        raise FileNotFoundError(f"No generation_results.json files found under {generation_root}")

    blocks, source_manifest = load_generation_blocks(files)
    coverage = validate_generation(blocks, args.expected_models, args.require_complete)

    if args.write_merged_generation:
        merged_path = outdir / "generation_results_merged.json"
        merged_path.write_text(json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8")

    generation_records = flatten_generation(blocks)
    generation_records.to_csv(outdir / "generation_records.csv", index=False)
    gen_overall, gen_category = aggregate_generation(generation_records)
    gen_overall.to_csv(outdir / "generation_metrics_by_model_architecture.csv", index=False)
    gen_category.to_csv(outdir / "generation_metrics_by_model_architecture_category.csv", index=False)

    combined = gen_overall.copy()
    combined_category = gen_category.copy()

    judge_path = Path(args.judge_results).resolve() if args.judge_results else None
    judge_df = load_judge_flat(judge_path)
    if judge_df is not None:
        judge_df.to_csv(outdir / "judge_records_normalized.csv", index=False)
        judge_overall, judge_category = aggregate_judge(judge_df)
        judge_overall.to_csv(outdir / "judge_metrics_by_model_architecture.csv", index=False)
        judge_category.to_csv(outdir / "judge_metrics_by_model_architecture_category.csv", index=False)
        combined = combined.merge(judge_overall, on=["Model", "Architecture"], how="left", validate="one_to_one")
        combined_category = combined_category.merge(judge_category, on=["Model", "Architecture", "Category"], how="left", validate="one_to_one")

    ood_dir = Path(args.ood_dir).resolve() if args.ood_dir else None
    ood_df = load_ood_detailed(ood_dir)
    if ood_df is not None:
        # OOD detailed is already one row per Model × Architecture.
        ood_df.to_csv(outdir / "ood_metrics_detailed_copy.csv", index=False)
        combined = combined.merge(ood_df, on=["Model", "Architecture"], how="left", validate="one_to_one")

    combined.to_csv(outdir / "final_metrics_by_model_architecture.csv", index=False)
    combined_category.to_csv(outdir / "final_metrics_by_model_architecture_category.csv", index=False)

    ablation = build_ablation_delta(combined)
    ablation.to_csv(outdir / "ablation_deltas.csv", index=False)

    # Architecture-level macro across generator models. We aggregate only numeric columns.
    numeric_cols = [c for c in combined.columns if c not in {"Model", "Architecture"} and pd.api.types.is_numeric_dtype(combined[c])]
    macro = combined.groupby("Architecture", sort=True)[numeric_cols].mean(numeric_only=True).reset_index()
    macro.to_csv(outdir / "final_metrics_macro_by_architecture.csv", index=False)

    manifest = {
        "analyser_version": ANALYSER_VERSION,
        "generation_root": str(generation_root),
        "generation_sources": source_manifest,
        "coverage": coverage,
        "judge_results": str(judge_path) if judge_path else None,
        "judge_results_sha256": _sha256(judge_path) if judge_path else None,
        "ood_dir": str(ood_dir) if ood_dir else None,
        "primary_architectures": PRIMARY_ARCHITECTURES,
        "faithfulness_policy": "faithfulness_valid uses explicit, semi-explicit, implicit only; anomalous/OOD excluded",
        "notes": [
            "No LLM or external inference is performed by analyser_metrics.py.",
            "Subtype means/rates use only applicable non-null judge records.",
            "Source generation files are read-only and never modified.",
        ],
    }
    (outdir / "analysis_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print("HydroGraphRAG deterministic aggregation complete")
    print(f"  Models: {coverage['model_count']}")
    print(f"  Architecture-query records: {coverage['architecture_query_records']}")
    print(f"  Output: {outdir}")
    print("  Main table: final_metrics_by_model_architecture.csv")
    print("  Category table: final_metrics_by_model_architecture_category.csv")
    print("  Ablations: ablation_deltas.csv")


if __name__ == "__main__":
    main()
