#!/usr/bin/env python3
"""
Export compact manuscript-ready HydroGraphRAG tables from analyser_metrics.py outputs.

This script DOES NOT call an LLM and DOES NOT recompute raw experiment outcomes.
It only reformats/aggregates already-computed deterministic/judge/OOD metrics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

EXPORT_VERSION = "hydrographrag-export-v2.0"

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


def read_csv(path: Path, required: bool = True) -> Optional[pd.DataFrame]:
    if not path.exists():
        if required:
            raise FileNotFoundError(path)
        return None
    return pd.read_csv(path)


def round_numeric(df: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].round(digits)
    return out


def pct(series: pd.Series) -> pd.Series:
    return series * 100.0


def existing(df: pd.DataFrame, columns: List[str]) -> List[str]:
    return [c for c in columns if c in df.columns]


def save(df: pd.DataFrame, path: Path, digits: int = 4) -> None:
    round_numeric(df, digits).to_csv(path, index=False)


def model_main_comparison(final_df: pd.DataFrame) -> pd.DataFrame:
    """Main-paper comparison: Baseline vs VectorRAG vs full HydroGraphRAG, per model."""
    df = final_df[final_df["Architecture"].isin(["Baseline", "VectorRAG", "HydroGraphRAG"])].copy()
    cols = [
        "Model", "Architecture", "N",
        "Entity_Precision_Mean", "Entity_Recall_Mean", "Entity_F1_Mean",
        "Semantic_Mean", "Structural_Mean", "Faithfulness_Valid_Mean",
        "Syntax_OK_Rate", "Exec_Success_Rate", "Map_Creation_Rate",
        "Total_Latency_Mean_s",
        "OOD_Precision", "OOD_Recall", "OOD_F1", "False_Rejection_Rate",
    ]
    return df[existing(df, cols)]


def architecture_macro(final_df: pd.DataFrame) -> pd.DataFrame:
    """Macro mean across seven generator models for all 9 architectures."""
    numeric = [c for c in final_df.columns if c not in {"Model", "Architecture"} and pd.api.types.is_numeric_dtype(final_df[c])]
    agg = final_df.groupby("Architecture", sort=False)[numeric].mean(numeric_only=True).reset_index()
    order = {a: i for i, a in enumerate(PRIMARY_ARCHITECTURES)}
    agg["_order"] = agg["Architecture"].map(order).fillna(999)
    return agg.sort_values("_order").drop(columns="_order")


def category_table(category_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "Model", "Architecture", "Category", "N",
        "Entity_Precision_Mean", "Entity_Recall_Mean", "Entity_F1_Mean",
        "Semantic_Mean", "Structural_Mean", "Faithfulness_Valid_Mean",
        "Spatial_Score_Mean", "Spatial_Hallucination_Rate",
        "Numerical_Score_Mean", "Numerical_Hallucination_Rate",
        "Temporal_Score_Mean", "Temporal_Hallucination_Rate",
        "Topological_Score_Mean", "Topological_Hallucination_Rate",
        "Categorical_Score_Mean", "Categorical_Hallucination_Rate",
        "Exec_Success_Rate", "Total_Latency_Mean_s",
    ]
    return category_df[existing(category_df, cols)]


def hallucination_table(final_df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Model", "Architecture"]
    for dim in ["Spatial", "Numerical", "Temporal", "Topological", "Categorical"]:
        cols += [f"{dim}_N", f"{dim}_Score_Mean", f"{dim}_Hallucination_Rate"]
    return final_df[existing(final_df, cols)]


def execution_table(final_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "Model", "Architecture", "N",
        "Syntax_OK_Rate", "Exec_Success_Rate", "Map_Creation_Rate",
        "Execution_Timeout_Rate",
        "CDA_Latency_Mean_s", "Retrieval_Latency_Mean_s",
        "Generation_Latency_Mean_s", "Execution_Latency_Mean_s",
        "Total_Latency_Mean_s", "Total_Latency_Median_s", "Total_Latency_Std_s",
    ]
    return final_df[existing(final_df, cols)]


def retrieval_table(final_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "Model", "Architecture", "Retrieval_N",
        "Entity_Precision_Mean", "Entity_Recall_Mean", "Entity_F1_Mean",
        "Targets_Found_Mean", "Retrieved_Entities_Mean", "Retrieved_Triples_Mean",
    ]
    df = final_df[existing(final_df, cols)].copy()
    if "Retrieval_N" in df.columns:
        df = df[df["Retrieval_N"].fillna(0) > 0]
    return df


def ood_table(final_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "Model", "Architecture",
        "Expected_OOD", "Expected_Valid", "TP", "FP", "TN", "FN",
        "OOD_Precision", "OOD_Recall", "OOD_F1", "False_Rejection_Rate",
        "False_Acceptance_Rate", "Specificity", "Accuracy", "Balanced_Accuracy",
        "Decision_Coverage", "Invalid_Decision_Rate", "Technical_Failure_Rate",
    ]
    return final_df[existing(final_df, cols)]


def ablation_table(ablation_df: pd.DataFrame) -> pd.DataFrame:
    return ablation_df.copy()


def make_percent_copy(df: pd.DataFrame) -> pd.DataFrame:
    """Human-readable percent copy for rate columns, while preserving score scales."""
    out = df.copy()
    rate_suffixes = ("_Rate", "_Coverage", "_Precision", "_Recall", "_F1", "_Accuracy", "Specificity", "Balanced_Accuracy")
    exclude = {"Entity_Precision_Mean", "Entity_Recall_Mean", "Entity_F1_Mean"}
    for c in out.columns:
        if c in exclude:
            # Retrieval metrics are also rates, so convert them intentionally.
            out[c] = pd.to_numeric(out[c], errors="coerce") * 100.0
        elif any(c.endswith(s) for s in rate_suffixes) or c in {
            "Syntax_OK_Rate", "Exec_Success_Rate", "Map_Creation_Rate",
            "Execution_Timeout_Rate", "False_Rejection_Rate", "False_Acceptance_Rate",
            "Decision_Coverage", "Invalid_Decision_Rate", "Technical_Failure_Rate",
            "OOD_Precision", "OOD_Recall", "OOD_F1", "Specificity", "Accuracy", "Balanced_Accuracy",
            "Spatial_Hallucination_Rate", "Numerical_Hallucination_Rate", "Temporal_Hallucination_Rate",
            "Topological_Hallucination_Rate", "Categorical_Hallucination_Rate",
        }:
            out[c] = pd.to_numeric(out[c], errors="coerce") * 100.0
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Export manuscript-ready HydroGraphRAG tables from analysis_outputs.")
    p.add_argument("--analysis-dir", default="analysis_outputs", help="Directory created by analyser_metrics.py")
    p.add_argument("--output-dir", default="exported_tables", help="Destination for compact paper/supplementary tables")
    args = p.parse_args()

    analysis_dir = Path(args.analysis_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    final_df = read_csv(analysis_dir / "final_metrics_by_model_architecture.csv")
    category_df = read_csv(analysis_dir / "final_metrics_by_model_architecture_category.csv")
    ablation_df = read_csv(analysis_dir / "ablation_deltas.csv", required=False)

    tables: Dict[str, pd.DataFrame] = {
        "table_main_comparison.csv": model_main_comparison(final_df),
        "table_architecture_macro.csv": architecture_macro(final_df),
        "table_retrieval.csv": retrieval_table(final_df),
        "table_execution_latency.csv": execution_table(final_df),
        "table_ood.csv": ood_table(final_df),
        "table_hallucination_subtypes.csv": hallucination_table(final_df),
        "table_by_category.csv": category_table(category_df),
    }
    if ablation_df is not None:
        tables["table_ablation_deltas.csv"] = ablation_table(ablation_df)

    for name, df in tables.items():
        save(df, output_dir / name)
        # Additional percent-formatted CSV for direct paper/chart use.
        save(make_percent_copy(df), output_dir / name.replace(".csv", "_percent.csv"), digits=2)

    # Per-model supplementary tables: all nine modes, compact and reproducible.
    supp_dir = output_dir / "supplementary_by_model"
    supp_dir.mkdir(exist_ok=True)
    for model, g in final_df.groupby("Model", sort=True):
        safe = str(model).replace(":", "_").replace("/", "_")
        order = {a: i for i, a in enumerate(PRIMARY_ARCHITECTURES)}
        gg = g.copy()
        gg["_order"] = gg["Architecture"].map(order).fillna(999)
        gg = gg.sort_values("_order").drop(columns="_order")
        save(gg, supp_dir / f"{safe}_all_architectures.csv")

    manifest: Dict[str, Any] = {
        "export_version": EXPORT_VERSION,
        "analysis_dir": str(analysis_dir),
        "output_dir": str(output_dir),
        "primary_architectures": PRIMARY_ARCHITECTURES,
        "main_paper_intent": {
            "table_main_comparison.csv": "Baseline vs VectorRAG vs full HydroGraphRAG by generator model",
            "table_architecture_macro.csv": "Macro mean across generator models for all nine architectures",
            "table_ablation_deltas.csv": "Full-minus-one ablation deltas relative to HydroGraphRAG",
            "table_ood.csv": "Structured ANSWER/ABSTAIN OOD metrics",
            "table_hallucination_subtypes.csv": "Applicable spatial/numerical/temporal/topological/categorical subtype scores and hallucination rates",
        },
        "notes": [
            "No AI inference is performed by export_tables.py.",
            "Files ending _percent.csv convert rate/proportion metrics from [0,1] to percentage points.",
            "Judge score scales (e.g. 1-5) are not converted to percentages.",
        ],
    }
    (output_dir / "export_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print("HydroGraphRAG table export complete")
    print(f"  Output: {output_dir}")
    for name in tables:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
