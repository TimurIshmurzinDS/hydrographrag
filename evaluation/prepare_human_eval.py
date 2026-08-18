from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import pandas as pd


GROUND_TRUTH = Path("ground_truth.json")
OUTPUT_DIR = Path("human_eval")

SAMPLE_FILE = OUTPUT_DIR / "human_eval_sample_30.csv"
SAMPLE_SHA_FILE = OUTPUT_DIR / "human_eval_sample_30.csv.sha256"
BLINDED_FILE = OUTPUT_DIR / "human_eval_blinded_90.xlsx"
UNBLINDED_FILE = OUTPUT_DIR / "human_eval_unblinded_90.xlsx"
BLINDING_KEY_FILE = OUTPUT_DIR / "human_eval_blinding_key.csv"
MISSING_OUTPUTS_FILE = OUTPUT_DIR / "human_eval_missing_outputs.csv"

SAMPLE_SEED = 42
BLINDING_SEED = 2026

SAMPLE_COUNTS = {
    "explicit": 10,
    "semi-explicit": 10,
    "implicit": 10,
}

ARCHITECTURES = [
    "Baseline",
    "VectorRAG",
    "HydroGraphRAG",
]

MODEL_NAME = "gemma2:27b"

RESULTS_ROOT = Path(
    "parallel_runs/gemma2_27b/results/gemma2_27b"
)


def normalize_category(value: str) -> str:
    value = str(value).strip().lower()
    replacements = {
        "semi_explicit": "semi-explicit",
        "semi explicit": "semi-explicit",
        "semiexplicit": "semi-explicit",
    }
    return replacements.get(value, value)


def id_sort_key(row: dict):
    value = str(row.get("id", ""))
    try:
        return (0, int(value))
    except ValueError:
        return (1, value)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ground_truth() -> list[dict]:
    if not GROUND_TRUTH.exists():
        raise FileNotFoundError(f"Ground truth not found: {GROUND_TRUTH}")

    with GROUND_TRUTH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("ground_truth.json must contain a JSON list.")

    return data


def get_query_text(row: dict) -> str:
    query = str(row.get("query", "")).strip()

    if not query:
        query = str(row.get("query_text", "")).strip()

    if not query:
        raise ValueError(f"Missing query text for ID={row.get('id')}")

    return query


def create_or_load_sample(ground_truth: list[dict]) -> pd.DataFrame:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if SAMPLE_FILE.exists():
        print(f"[INFO] Frozen sample already exists: {SAMPLE_FILE}")
        print("[INFO] Reusing it. No re-sampling performed.")

        sample_df = pd.read_csv(
            SAMPLE_FILE,
            dtype={"query_id": str},
        )

        verify_sample(sample_df)
        return sample_df

    rng = random.Random(SAMPLE_SEED)
    selected_rows = []

    for category, required_n in SAMPLE_COUNTS.items():
        pool = [
            row
            for row in ground_truth
            if normalize_category(row.get("category", "")) == category
            and str(row.get("expected_decision", "")).strip().upper() == "ANSWER"
        ]

        pool = sorted(pool, key=id_sort_key)

        if len(pool) < required_n:
            raise RuntimeError(
                f"Not enough valid queries for {category}: "
                f"required={required_n}, available={len(pool)}"
            )

        chosen = rng.sample(pool, required_n)

        for row in chosen:
            selected_rows.append(
                {
                    "query_id": str(row["id"]),
                    "category": category,
                    "query_text": get_query_text(row),
                }
            )

    category_order = {
        "explicit": 0,
        "semi-explicit": 1,
        "implicit": 2,
    }

    selected_rows.sort(
        key=lambda r: (
            category_order[r["category"]],
            int(r["query_id"]) if r["query_id"].isdigit() else r["query_id"],
        )
    )

    sample_df = pd.DataFrame(selected_rows)
    verify_sample(sample_df)

    sample_df.to_csv(
        SAMPLE_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    digest = sha256_file(SAMPLE_FILE)

    SAMPLE_SHA_FILE.write_text(
        f"{digest}  {SAMPLE_FILE.name}\n",
        encoding="utf-8",
    )

    print()
    print("========================================")
    print("FROZEN HUMAN-EVAL SAMPLE CREATED")
    print("========================================")
    print(f"Seed:     {SAMPLE_SEED}")
    print(f"File:     {SAMPLE_FILE}")
    print(f"SHA256:   {digest}")
    print()

    return sample_df


def verify_sample(sample_df: pd.DataFrame) -> None:
    required_columns = {
        "query_id",
        "category",
        "query_text",
    }

    missing_columns = required_columns - set(sample_df.columns)

    if missing_columns:
        raise RuntimeError(
            f"Sample file missing columns: {sorted(missing_columns)}"
        )

    if len(sample_df) != 30:
        raise RuntimeError(
            f"Expected 30 sampled queries, found {len(sample_df)}"
        )

    if sample_df["query_id"].astype(str).duplicated().any():
        raise RuntimeError("Duplicate query IDs found in human sample.")

    normalized = sample_df["category"].map(normalize_category)
    counts = normalized.value_counts().to_dict()

    for category, expected_n in SAMPLE_COUNTS.items():
        actual_n = int(counts.get(category, 0))

        if actual_n != expected_n:
            raise RuntimeError(
                f"Invalid sample distribution for {category}: "
                f"expected={expected_n}, actual={actual_n}"
            )


def build_gt_lookup(ground_truth: list[dict]) -> dict[str, dict]:
    result = {}

    for row in ground_truth:
        qid = str(row.get("id", "")).strip()
        if qid:
            result[qid] = row

    return result


def compact_reference_evidence(row: dict) -> str:
    parts = []

    entities = row.get("expected_entities", [])
    if entities:
        parts.append("Expected entities: " + "; ".join(map(str, entities)))

    numeric = row.get("expected_numeric_facts", [])
    if numeric:
        parts.append(
            "Numeric evidence: "
            + json.dumps(numeric, ensure_ascii=False)
        )

    temporal = row.get("expected_temporal_facts", [])
    if temporal:
        parts.append(
            "Temporal evidence: "
            + json.dumps(temporal, ensure_ascii=False)
        )

    topology = row.get("expected_topology", [])
    if topology:
        parts.append(
            "Topological evidence: "
            + json.dumps(topology, ensure_ascii=False)
        )

    categories = row.get("expected_categories", [])
    if categories:
        parts.append(
            "Categorical evidence: "
            + json.dumps(categories, ensure_ascii=False)
        )

    missing = row.get("expected_missing_facts", [])
    if missing:
        parts.append(
            "Requested evidence unavailable in benchmark: "
            + json.dumps(missing, ensure_ascii=False)
        )

    requirements = row.get("query_requirements", {}) or {}

    if requirements.get("spatial"):
        expected_wkt = row.get("expected_wkt", [])
        if expected_wkt:
            parts.append(
                "Spatial evidence (WKT): "
                + "; ".join(map(str, expected_wkt))
            )

    if not parts:
        return "No additional structured reference evidence is available."

    return "\n".join(parts)


def check_available_outputs(
    sample_df: pd.DataFrame,
) -> tuple[list[dict], list[dict]]:
    ready = []
    missing = []

    for _, row in sample_df.iterrows():
        query_id = str(row["query_id"])
        category = normalize_category(row["category"])

        for architecture in ARCHITECTURES:
            artifact_dir = RESULTS_ROOT / architecture / query_id
            response_path = artifact_dir / "response.txt"
            metadata_path = artifact_dir / "metadata.json"

            if not response_path.exists() or not metadata_path.exists():
                missing.append(
                    {
                        "query_id": query_id,
                        "category": category,
                        "architecture": architecture,
                        "response_exists": response_path.exists(),
                        "metadata_exists": metadata_path.exists(),
                    }
                )
                continue

            ready.append(
                {
                    "query_id": query_id,
                    "category": category,
                    "architecture": architecture,
                    "artifact_dir": artifact_dir,
                    "response_path": response_path,
                    "metadata_path": metadata_path,
                }
            )

    return ready, missing


def collect_records(
    sample_df: pd.DataFrame,
    ground_truth: list[dict],
) -> list[dict]:
    gt_lookup = build_gt_lookup(ground_truth)
    records = []

    for _, sample_row in sample_df.iterrows():
        query_id = str(sample_row["query_id"])
        gt_row = gt_lookup.get(query_id)

        if gt_row is None:
            raise RuntimeError(f"Query {query_id} not found in ground truth.")

        for architecture in ARCHITECTURES:
            artifact_dir = RESULTS_ROOT / architecture / query_id
            response_path = artifact_dir / "response.txt"
            metadata_path = artifact_dir / "metadata.json"

            generated_answer = response_path.read_text(
                encoding="utf-8",
                errors="replace",
            ).strip()

            with metadata_path.open("r", encoding="utf-8") as f:
                metadata = json.load(f)

            if str(metadata.get("model")) != MODEL_NAME:
                raise RuntimeError(
                    f"Model mismatch in {metadata_path}: "
                    f"{metadata.get('model')!r}"
                )

            if str(metadata.get("architecture")) != architecture:
                raise RuntimeError(
                    f"Architecture mismatch in {metadata_path}"
                )

            if str(metadata.get("query_id")) != query_id:
                raise RuntimeError(
                    f"Query ID mismatch in {metadata_path}"
                )

            html_files = sorted(artifact_dir.glob("*.html"))
            map_path = str(html_files[0]) if html_files else ""

            result = metadata.get("result", {}) or {}

            records.append(
                {
                    "query_id": query_id,
                    "category": normalize_category(sample_row["category"]),
                    "query_text": str(sample_row["query_text"]),
                    "gold_reference_evidence": compact_reference_evidence(gt_row),
                    "generated_answer": generated_answer,
                    "generated_map_path": map_path,
                    "model": MODEL_NAME,
                    "architecture": architecture,
                    "decision": result.get("decision", ""),
                    "artifact_path": str(artifact_dir),
                }
            )

    if len(records) != 90:
        raise RuntimeError(
            f"Expected 90 records, found {len(records)}"
        )

    return records


def assign_blinded_ids(records: list[dict]) -> list[dict]:
    records = [dict(record) for record in records]

    rng = random.Random(BLINDING_SEED)
    rng.shuffle(records)

    for index, record in enumerate(records, start=1):
        record["Eval_ID"] = f"EVAL-{index:03d}"
        record["Output_Order"] = index

    return records


def write_blinding_key(records: list[dict]) -> None:
    key_rows = []

    for record in records:
        key_rows.append(
            {
                "Eval_ID": record["Eval_ID"],
                "Output_Order": record["Output_Order"],
                "query_id": record["query_id"],
                "category": record["category"],
                "model": record["model"],
                "architecture": record["architecture"],
                "decision": record["decision"],
                "artifact_path": record["artifact_path"],
            }
        )

    pd.DataFrame(key_rows).to_csv(
        BLINDING_KEY_FILE,
        index=False,
        encoding="utf-8-sig",
    )


def write_excel_files(records: list[dict]) -> None:
    blinded_rows = []

    for record in records:
        blinded_rows.append(
            {
                "Eval_ID": record["Eval_ID"],
                "Category": record["category"],
                "Query_Text": record["query_text"],
                "Gold_Reference_Evidence": record["gold_reference_evidence"],
                "Generated_Answer": record["generated_answer"],
                "Factual_Correctness_1_5": "",
                "Evidence_Faithfulness_1_5": "",
                "Hydrological_Relevance_1_5": "",
                "GIS_Correctness_1_5_or_NA": "",
                "Overall_Quality_1_5": "",
                "Comments": "",
            }
        )

    blinded_df = pd.DataFrame(blinded_rows)

    unblinded_rows = []

    for record in records:
        unblinded_rows.append(
            {
                "Eval_ID": record["Eval_ID"],
                "Output_Order": record["Output_Order"],
                "Query_ID": record["query_id"],
                "Category": record["category"],
                "Query_Text": record["query_text"],
                "Model": record["model"],
                "Architecture": record["architecture"],
                "Decision": record["decision"],
                "Gold_Reference_Evidence": record["gold_reference_evidence"],
                "Generated_Answer": record["generated_answer"],
                "Generated_Map_Path": record["generated_map_path"],
                "Artifact_Path": record["artifact_path"],
            }
        )

    unblinded_df = pd.DataFrame(unblinded_rows)

    instructions_df = pd.DataFrame(
        {
            "Human Evaluation Instructions": [
                "Responses are anonymized and randomized.",
                "Evaluate each response independently.",
                "Architecture and generator identity are intentionally hidden.",
                "Use the supplied query and reference evidence.",
                "1 = very poor / incorrect",
                "2 = poor",
                "3 = acceptable",
                "4 = good",
                "5 = excellent",
                "GIS correctness may be marked N/A when not applicable.",
            ]
        }
    )

    with pd.ExcelWriter(
        BLINDED_FILE,
        engine="openpyxl",
    ) as writer:
        blinded_df.to_excel(
            writer,
            sheet_name="Human Evaluation",
            index=False,
        )
        instructions_df.to_excel(
            writer,
            sheet_name="Instructions",
            index=False,
        )

    with pd.ExcelWriter(
        UNBLINDED_FILE,
        engine="openpyxl",
    ) as writer:
        unblinded_df.to_excel(
            writer,
            sheet_name="Master",
            index=False,
        )


def main():
    print()
    print("========================================")
    print("HydroGraphRAG Human Evaluation Builder")
    print("========================================")
    print()

    ground_truth = load_ground_truth()

    sample_df = create_or_load_sample(ground_truth)

    print("Selected query distribution:")
    print(sample_df["category"].value_counts())

    print()
    print("Selected query IDs:")
    print(
        sample_df[
            ["query_id", "category"]
        ].to_string(index=False)
    )

    ready, missing = check_available_outputs(sample_df)

    print()
    print("========================================")
    print("GEMMA HUMAN-EVAL READINESS")
    print("========================================")
    print(f"Ready outputs:   {len(ready)}/90")
    print(f"Missing outputs: {len(missing)}/90")

    if missing:
        missing_df = pd.DataFrame(missing)

        missing_df.to_csv(
            MISSING_OUTPUTS_FILE,
            index=False,
            encoding="utf-8-sig",
        )

        print()
        print("Not all sampled outputs have been generated yet.")
        print(
            "IMPORTANT: the frozen 30-query sample "
            "will NOT be changed."
        )
        print(
            f"Missing-output report: "
            f"{MISSING_OUTPUTS_FILE}"
        )
        print()
        print(
            "Run this script again later after Gemma "
            "has generated the missing outputs."
        )
        return

    if MISSING_OUTPUTS_FILE.exists():
        MISSING_OUTPUTS_FILE.unlink()

    records = collect_records(
        sample_df,
        ground_truth,
    )

    records = assign_blinded_ids(records)

    write_blinding_key(records)
    write_excel_files(records)

    print()
    print("========================================")
    print("HUMAN-EVAL PACKAGE CREATED")
    print("========================================")
    print(f"Sample:       {SAMPLE_FILE}")
    print(f"Sample SHA:   {SAMPLE_SHA_FILE}")
    print(f"Blinded:      {BLINDED_FILE}")
    print(f"Unblinded:    {UNBLINDED_FILE}")
    print(f"Blinding key: {BLINDING_KEY_FILE}")
    print()
    print("IMPORTANT:")
    print(
        "Give ONLY human_eval_blinded_90.xlsx "
        "to experts."
    )
    print(
        "Keep human_eval_unblinded_90.xlsx and "
        "human_eval_blinding_key.csv internal."
    )


if __name__ == "__main__":
    main()
