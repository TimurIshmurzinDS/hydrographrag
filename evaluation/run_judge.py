#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HydroGraphRAG final judge runner.

Purpose
-------
Evaluate generated answers/code against the frozen HydroGraphRAG gold benchmark
without leaking architecture labels into the judge prompt.

Main principles
---------------
1. Frozen gold is read-only.
2. Judge failures never become valid scores.
3. Empty gold fields do NOT imply a perfect score.
4. OOD decision evaluation is separated from answer faithfulness.
5. Hallucination subtypes are reported explicitly.
6. expected_missing_facts is used to detect unsupported claims.
7. Exact judge prompts, hashes, raw outputs, and parsed outputs are persisted.
8. The judge never modifies generation outputs or benchmark files.

Expected generation layout
--------------------------
The script searches recursively below --results-root for JSON files that look like
generation results. It supports either:
  results/<model>/<mode>/<id>.json
or any equivalent nested layout.

Each result should ideally contain:
  id / query_id
  query
  model
  mode / architecture
  decision
  raw_response / response / answer
  code
  retrieved_entities
  retrieved_triples
  retrieval_context
  failure_type / status

The runner is deliberately permissive about field names and stores warnings when
fields are absent.

Default judge
-------------
qwen2.5:72b-instruct via Ollama HTTP API.

No human evaluation is implemented here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests


# ============================================================
# CONFIG
# ============================================================

JUDGE_SCRIPT_VERSION = "hydrographrag_judge_v4"
JUDGE_PROMPT_VERSION = "hydrographrag_judge_prompt_v4"

DEFAULT_GROUND_TRUTH = "ground_truth.json"
DEFAULT_RESULTS_ROOT = "results"
DEFAULT_OUTPUT_ROOT = "judge_results"

OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"

DEFAULT_JUDGE_MODEL = "qwen2.5:72b-instruct"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_TOP_P = 1.0
DEFAULT_SEED = 42
DEFAULT_NUM_CTX = 8192
DEFAULT_TIMEOUT = 180

VALID_DECISIONS = {"ANSWER", "ABSTAIN"}
VALID_CATEGORIES = {
    "explicit",
    "semi-explicit",
    "implicit",
    "anomalous",
}

# Score scale is retained for comparability with the previous manuscript,
# but applicability is now explicit.
SCORE_MIN = 1
SCORE_MAX = 5


# ============================================================
# UTILITIES
# ============================================================

def utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def normalize_decision(value: Any) -> str:
    text = normalize_text(value).upper()

    if "ABSTAIN" in text:
        return "ABSTAIN"

    if "ANSWER" in text:
        return "ANSWER"

    return "INVALID"


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def json_dumps_compact(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def unique_preserve(values: Sequence[Any]) -> List[Any]:
    result = []
    seen = set()

    for value in values:
        key = json_dumps_compact(value)

        if key in seen:
            continue

        seen.add(key)
        result.append(value)

    return result


def safe_mean(values: Sequence[float]) -> Optional[float]:
    clean = [
        float(v)
        for v in values
        if v is not None
        and not math.isnan(float(v))
    ]

    if not clean:
        return None

    return sum(clean) / len(clean)


def safe_stdev(values: Sequence[float]) -> Optional[float]:
    clean = [
        float(v)
        for v in values
        if v is not None
        and not math.isnan(float(v))
    ]

    if len(clean) < 2:
        return 0.0 if clean else None

    return statistics.stdev(clean)


def local_name(uri: Any) -> str:
    text = str(uri or "").strip()

    if "#" in text:
        return text.rsplit("#", 1)[-1]

    if "/" in text:
        return text.rstrip("/").rsplit("/", 1)[-1]

    return text


def ensure_dir(path: Path) -> None:
    path.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# FROZEN GOLD
# ============================================================

def load_ground_truth(
    path: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        payload = json.load(f)

    if not isinstance(payload, list):
        raise ValueError(
            "ground_truth.json must contain a JSON list."
        )

    by_id: Dict[str, Dict[str, Any]] = {}

    for item in payload:
        if not isinstance(item, dict):
            raise ValueError(
                "Every ground-truth item must be an object."
            )

        query_id = str(
            item.get(
                "id",
                "",
            )
        ).strip()

        if not query_id:
            raise ValueError(
                "Ground-truth item missing id."
            )

        if query_id in by_id:
            raise ValueError(
                f"Duplicate ground-truth id: {query_id}"
            )

        by_id[query_id] = item

    return payload, by_id


# ============================================================
# GENERATION RESULT DISCOVERY
# ============================================================

def looks_like_generation_result(
    payload: Any,
) -> bool:
    if not isinstance(payload, dict):
        return False

    keys = {
        str(k).lower()
        for k in payload.keys()
    }

    id_like = bool(
        {
            "id",
            "query_id",
        }
        & keys
    )

    output_like = bool(
        {
            "raw_response",
            "response",
            "answer",
            "generated_response",
            "code",
            "decision",
        }
        & keys
    )

    return id_like and output_like


def discover_generation_files(
    results_root: Path,
) -> List[Path]:
    files = []

    for path in results_root.rglob("*.json"):
        name = path.name.lower()

        if (
            "manifest" in name
            or "judge" in name
            or "summary" in name
            or "ground_truth" in name
        ):
            continue

        try:
            with path.open(
                "r",
                encoding="utf-8",
            ) as f:
                payload = json.load(f)
        except Exception:
            continue

        if looks_like_generation_result(
            payload
        ):
            files.append(path)

    return sorted(files)


def read_generation_result(
    path: Path,
) -> Dict[str, Any]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError(
            f"Generation file is not a JSON object: {path}"
        )

    return payload


def infer_query_id(
    result: Dict[str, Any],
    path: Path,
) -> str:
    for key in [
        "query_id",
        "id",
    ]:
        if key in result:
            value = str(
                result.get(key)
            ).strip()

            if value:
                return value

    stem_match = re.search(
        r"(\d+)",
        path.stem,
    )

    if stem_match:
        return stem_match.group(1)

    return ""


def infer_model(
    result: Dict[str, Any],
    path: Path,
    results_root: Path,
) -> str:
    for key in [
        "model",
        "model_name",
        "generator_model",
    ]:
        value = normalize_text(
            result.get(key)
        )

        if value:
            return value

    try:
        relative = path.relative_to(
            results_root
        )

        if len(
            relative.parts
        ) >= 3:
            return relative.parts[0]
    except Exception:
        pass

    return "unknown_model"


def infer_mode(
    result: Dict[str, Any],
    path: Path,
    results_root: Path,
) -> str:
    for key in [
        "mode",
        "architecture",
        "architecture_mode",
        "eval_mode",
    ]:
        value = normalize_text(
            result.get(key)
        )

        if value:
            return value

    try:
        relative = path.relative_to(
            results_root
        )

        if len(
            relative.parts
        ) >= 3:
            return relative.parts[1]
    except Exception:
        pass

    return "unknown_mode"


def extract_generated_text(
    result: Dict[str, Any],
) -> str:
    candidates = []

    for key in [
        "raw_response",
        "generated_response",
        "response",
        "answer",
        "model_output",
        "text",
    ]:
        value = result.get(key)

        if isinstance(
            value,
            str,
        ) and value.strip():
            candidates.append(
                value.strip()
            )

    # If only code exists, judge still needs to inspect it.
    code = result.get(
        "code"
    )

    if isinstance(
        code,
        str,
    ) and code.strip():
        candidates.append(
            "IMPLEMENTATION CODE:\n"
            + code.strip()
        )

    return "\n\n".join(
        unique_preserve(
            candidates
        )
    ).strip()


def extract_decision(
    result: Dict[str, Any],
    generated_text: str,
) -> str:
    direct = result.get(
        "decision"
    )

    normalized = normalize_decision(
        direct
    )

    if normalized != "INVALID":
        return normalized

    match = re.search(
        r"(?im)^\s*decision\s*:\s*(ANSWER|ABSTAIN)\b",
        generated_text,
    )

    if match:
        return match.group(1).upper()

    return "INVALID"


def extract_retrieved_evidence(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    entities = result.get(
        "retrieved_entities",
        [],
    )

    triples = result.get(
        "retrieved_triples",
        [],
    )

    context = result.get(
        "retrieval_context",
        result.get(
            "context",
            "",
        ),
    )

    if not isinstance(
        entities,
        list,
    ):
        entities = []

    if not isinstance(
        triples,
        list,
    ):
        triples = []

    return {
        "retrieved_entities": entities,
        "retrieved_triples": triples,
        "retrieval_context": context,
    }


# ============================================================
# GOLD PROJECTION FOR JUDGE
# ============================================================

def gold_applicability(
    gold: Dict[str, Any],
) -> Dict[str, bool]:
    requirements = gold.get(
        "query_requirements",
        {},
    )

    if not isinstance(
        requirements,
        dict,
    ):
        requirements = {}

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

    return {
        "ood": (
            category == "anomalous"
            or expected_decision == "ABSTAIN"
        ),
        "entity": bool(
            requirements.get(
                "entity",
                True,
            )
        ),
        "spatial": bool(
            requirements.get(
                "spatial",
                False,
            )
            or gold.get(
                "expected_wkt"
            )
        ),
        "numerical": bool(
            requirements.get(
                "numeric",
                False,
            )
        ),
        "temporal": bool(
            requirements.get(
                "temporal",
                False,
            )
        ),
        "topological": bool(
            requirements.get(
                "topological",
                False,
            )
        ),
        "categorical": bool(
            requirements.get(
                "categorical",
                False,
            )
        ),
    }


def build_gold_for_judge(
    gold: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Keep only fields relevant for judging.
    Do not include architecture/model metadata.
    """

    return {
        "query": gold.get(
            "query",
            "",
        ),
        "category": gold.get(
            "category",
            "",
        ),
        "expected_decision": gold.get(
            "expected_decision",
            "",
        ),
        "query_requirements": gold.get(
            "query_requirements",
            {},
        ),
        "expected_entities": gold.get(
            "expected_entities",
            [],
        ),
        "expected_entity_iris": gold.get(
            "expected_entity_iris",
            [],
        ),
        "expected_relations": gold.get(
            "expected_relations",
            [],
        ),
        "expected_triples": gold.get(
            "expected_triples",
            [],
        ),
        "expected_wkt": gold.get(
            "expected_wkt",
            [],
        ),
        "expected_numeric_facts": gold.get(
            "expected_numeric_facts",
            [],
        ),
        "expected_temporal_facts": gold.get(
            "expected_temporal_facts",
            [],
        ),
        "expected_categories": gold.get(
            "expected_categories",
            [],
        ),
        "expected_topology": gold.get(
            "expected_topology",
            [],
        ),
        "expected_missing_facts": gold.get(
            "expected_missing_facts",
            [],
        ),
        "per_entity_coverage": (
            gold.get(
                "gold_evidence_summary",
                {},
            ).get(
                "per_entity_coverage",
                [],
            )
            if isinstance(
                gold.get(
                    "gold_evidence_summary",
                    {},
                ),
                dict,
            )
            else []
        ),
        "gold_review": {
            "needs_manual_review": bool(
                gold.get(
                    "gold_review",
                    {},
                ).get(
                    "needs_manual_review",
                    False,
                )
            )
            if isinstance(
                gold.get(
                    "gold_review",
                    {},
                ),
                dict,
            )
            else False,
            "reasons": (
                gold.get(
                    "gold_review",
                    {},
                ).get(
                    "reasons",
                    [],
                )
                if isinstance(
                    gold.get(
                        "gold_review",
                        {},
                    ),
                    dict,
                )
                else []
            ),
        },
    }


# ============================================================
# DETERMINISTIC PRE-JUDGE CHECKS
# ============================================================

def text_contains_any(
    text: str,
    values: Sequence[str],
) -> bool:
    normalized = text.lower()

    return any(
        str(value).strip().lower()
        in normalized
        for value in values
        if str(value).strip()
    )


def deterministic_checks(
    gold: Dict[str, Any],
    generated_text: str,
    decision: str,
) -> Dict[str, Any]:
    expected_decision = normalize_decision(
        gold.get(
            "expected_decision"
        )
    )

    expected_entities = [
        str(v)
        for v in gold.get(
            "expected_entities",
            []
        )
        if str(v).strip()
    ]

    expected_wkt = [
        str(v)
        for v in gold.get(
            "expected_wkt",
            []
        )
        if str(v).strip()
    ]

    entity_mentions = {
        entity: (
            entity.lower()
            in generated_text.lower()
        )
        for entity in expected_entities
    }

    wkt_mentions = {
        wkt: (
            wkt.lower()
            in generated_text.lower()
        )
        for wkt in expected_wkt
    }

    return {
        "expected_decision": expected_decision,
        "actual_decision": decision,
        "decision_correct": (
            decision == expected_decision
            if decision in VALID_DECISIONS
            and expected_decision in VALID_DECISIONS
            else False
        ),
        "decision_valid": (
            decision
            in VALID_DECISIONS
        ),
        "entity_mentions": entity_mentions,
        "all_expected_entities_mentioned": (
            all(
                entity_mentions.values()
            )
            if entity_mentions
            else None
        ),
        "wkt_mentions": wkt_mentions,
        "all_expected_wkt_mentioned": (
            all(
                wkt_mentions.values()
            )
            if wkt_mentions
            else None
        ),
    }


# ============================================================
# JUDGE PROMPT
# ============================================================

JUDGE_SYSTEM_INSTRUCTION = r"""
You are an evaluator for a hydrology/GIS retrieval-augmented generation benchmark.

Your task is to assess one generated response against a frozen gold evidence package.

IMPORTANT RULES:

1. Judge only from the supplied GOLD EVIDENCE and GENERATED RESPONSE.
2. Do not reward unsupported plausible hydrological knowledge.
3. Do not infer that an empty gold subtype means the response is perfect.
4. A subtype with applicable=false MUST have score=null.
5. If applicable=true but the gold explicitly says the requested fact is missing,
   then a grounded response should acknowledge unavailability or insufficiency.
   Inventing a value/status/relation in that case is a hallucination.
6. OOD decision correctness is separate from answer faithfulness.
7. If expected_decision=ABSTAIN:
   - judge decision correctness;
   - do not assign ordinary answer faithfulness scores unless the response makes
     substantive unsupported hydrological claims despite abstaining.
8. For valid in-domain queries with missing evidence:
   - ANSWER can still be correct;
   - saying the requested fact is unavailable is acceptable;
   - fabricating it is not.
9. Spatial hallucination includes invented/altered WKT, coordinates, geometry,
   spatial intersection, distance, proximity, or location unsupported by gold.
10. Numerical hallucination includes invented or altered measurements, thresholds,
    averages, trends, probabilities, discharge, water levels, or other quantities.
11. Temporal hallucination includes invented dates, periods, recency, historical
    windows, seasonality, or claiming real-time/current status beyond the frozen
    snapshot evidence.
12. Topological hallucination includes invented upstream/downstream/tributary,
    flows-into, network hierarchy, connectivity, propagation path, or watershed
    relation unsupported by gold.
13. Categorical hallucination includes invented water-quality/status/class/risk/
    operational labels unsupported by gold.
14. Give a score only for applicable dimensions.

SCORING SCALE (1-5):
5 = fully supported and correct
4 = mostly supported, minor omission/imprecision
3 = mixed; meaningful supported content plus notable issue
2 = major unsupported/incomplete content
1 = fundamentally incorrect or hallucinated

Return STRICT JSON only. No markdown, no explanation outside JSON.
"""


def build_judge_prompt(
    gold: Dict[str, Any],
    generated_text: str,
    decision: str,
    retrieved_evidence: Dict[str, Any],
) -> str:
    applicability = gold_applicability(
        gold
    )

    gold_package = build_gold_for_judge(
        gold
    )

    prompt_payload = {
        "judge_prompt_version": (
            JUDGE_PROMPT_VERSION
        ),
        "applicability": applicability,
        "gold_evidence": gold_package,
        "generated_response": generated_text,
        "generated_decision": decision,
        # Retrieval context is supplied only as supporting provenance.
        # It is NOT ground truth.
        "retrieved_evidence_for_context_only": {
            "retrieved_entities": (
                retrieved_evidence.get(
                    "retrieved_entities",
                    [],
                )
            ),
            "retrieved_triples": (
                retrieved_evidence.get(
                    "retrieved_triples",
                    [],
                )
            ),
        },
        "required_output_schema": {
            "decision": {
                "expected": "ANSWER|ABSTAIN",
                "actual": "ANSWER|ABSTAIN|INVALID",
                "correct": True,
                "reason": "short string",
            },
            "semantic": {
                "applicable": True,
                "score": 1,
                "reason": "short string",
            },
            "structural": {
                "applicable": True,
                "score": 1,
                "reason": "short string",
            },
            "faithfulness": {
                "applicable": True,
                "score": 1,
                "reason": "short string",
            },
            "subtypes": {
                "spatial": {
                    "applicable": False,
                    "score": None,
                    "hallucination": False,
                    "severity": 0,
                    "claims": [],
                    "reason": "short string",
                },
                "numerical": {
                    "applicable": False,
                    "score": None,
                    "hallucination": False,
                    "severity": 0,
                    "claims": [],
                    "reason": "short string",
                },
                "temporal": {
                    "applicable": False,
                    "score": None,
                    "hallucination": False,
                    "severity": 0,
                    "claims": [],
                    "reason": "short string",
                },
                "topological": {
                    "applicable": False,
                    "score": None,
                    "hallucination": False,
                    "severity": 0,
                    "claims": [],
                    "reason": "short string",
                },
                "categorical": {
                    "applicable": False,
                    "score": None,
                    "hallucination": False,
                    "severity": 0,
                    "claims": [],
                    "reason": "short string",
                },
            },
            "unsupported_claims": [],
            "missing_required_content": [],
            "overall_notes": "short string",
        },
    }

    return (
        JUDGE_SYSTEM_INSTRUCTION.strip()
        + "\n\nINPUT:\n"
        + json.dumps(
            prompt_payload,
            ensure_ascii=False,
            indent=2,
        )
    )


# ============================================================
# OLLAMA
# ============================================================

class OllamaJudge:

    def __init__(
        self,
        model: str,
        temperature: float,
        top_p: float,
        seed: int,
        num_ctx: int,
        timeout: int,
    ):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed
        self.num_ctx = num_ctx
        self.timeout = timeout
        self.session = requests.Session()

    def generate(
        self,
        prompt: str,
    ) -> Tuple[str, Dict[str, Any]]:
        started = time.perf_counter()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": (
                    self.temperature
                ),
                "top_p": (
                    self.top_p
                ),
                "seed": (
                    self.seed
                ),
                "num_ctx": (
                    self.num_ctx
                ),
            },
        }

        response = self.session.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            timeout=self.timeout,
        )

        elapsed = (
            time.perf_counter()
            - started
        )

        response.raise_for_status()

        body = response.json()

        raw = body.get(
            "response",
            "",
        )

        metadata = {
            "latency_s": elapsed,
            "done": body.get(
                "done"
            ),
            "done_reason": body.get(
                "done_reason"
            ),
            "total_duration": body.get(
                "total_duration"
            ),
            "load_duration": body.get(
                "load_duration"
            ),
            "prompt_eval_count": body.get(
                "prompt_eval_count"
            ),
            "prompt_eval_duration": body.get(
                "prompt_eval_duration"
            ),
            "eval_count": body.get(
                "eval_count"
            ),
            "eval_duration": body.get(
                "eval_duration"
            ),
        }

        return raw, metadata


# ============================================================
# STRICT PARSING / VALIDATION
# ============================================================

def parse_json_object(
    raw: str,
) -> Dict[str, Any]:
    text = raw.strip()

    if not text:
        raise ValueError(
            "Judge returned empty output."
        )

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        # Conservative extraction fallback.
        first = text.find("{")
        last = text.rfind("}")

        if (
            first < 0
            or last <= first
        ):
            raise

        payload = json.loads(
            text[
                first:last + 1
            ]
        )

    if not isinstance(
        payload,
        dict,
    ):
        raise ValueError(
            "Judge output must be a JSON object."
        )

    return payload


def validate_score(
    value: Any,
    applicable: bool,
    field_name: str,
) -> Optional[float]:
    if not applicable:
        if value is not None:
            raise ValueError(
                f"{field_name}: score must be null when applicable=false."
            )

        return None

    if value is None:
        raise ValueError(
            f"{field_name}: missing score for applicable dimension."
        )

    try:
        score = float(value)
    except Exception as exc:
        raise ValueError(
            f"{field_name}: non-numeric score: {value!r}"
        ) from exc

    if not (
        SCORE_MIN
        <= score
        <= SCORE_MAX
    ):
        raise ValueError(
            f"{field_name}: score out of range: {score}"
        )

    return score


def validate_dimension(
    payload: Dict[str, Any],
    name: str,
) -> Dict[str, Any]:
    value = payload.get(
        name
    )

    if not isinstance(
        value,
        dict,
    ):
        raise ValueError(
            f"Missing dimension object: {name}"
        )

    applicable = bool(
        value.get(
            "applicable",
            False,
        )
    )

    score = validate_score(
        value.get(
            "score"
        ),
        applicable,
        name,
    )

    return {
        "applicable": applicable,
        "score": score,
        "reason": normalize_text(
            value.get(
                "reason"
            )
        ),
    }


def validate_subtype(
    payload: Dict[str, Any],
    name: str,
) -> Dict[str, Any]:
    subtypes = payload.get(
        "subtypes"
    )

    if not isinstance(
        subtypes,
        dict,
    ):
        raise ValueError(
            "Missing subtypes object."
        )

    value = subtypes.get(
        name
    )

    if not isinstance(
        value,
        dict,
    ):
        raise ValueError(
            f"Missing subtype object: {name}"
        )

    applicable = bool(
        value.get(
            "applicable",
            False,
        )
    )

    score = validate_score(
        value.get(
            "score"
        ),
        applicable,
        f"subtypes.{name}",
    )

    hallucination = bool(
        value.get(
            "hallucination",
            False,
        )
    )

    try:
        severity = int(
            value.get(
                "severity",
                0,
            )
        )
    except Exception as exc:
        raise ValueError(
            f"Invalid severity for {name}."
        ) from exc

    if severity < 0 or severity > 3:
        raise ValueError(
            f"Severity must be 0..3 for {name}."
        )

    claims = value.get(
        "claims",
        [],
    )

    if not isinstance(
        claims,
        list,
    ):
        claims = [
            str(claims)
        ]

    return {
        "applicable": applicable,
        "score": score,
        "hallucination": (
            hallucination
        ),
        "severity": severity,
        "claims": [
            normalize_text(v)
            for v in claims
            if normalize_text(v)
        ],
        "reason": normalize_text(
            value.get(
                "reason"
            )
        ),
    }


def validate_judge_payload(
    payload: Dict[str, Any],
    expected_applicability: Dict[str, bool],
) -> Dict[str, Any]:
    decision_payload = payload.get(
        "decision"
    )

    if not isinstance(
        decision_payload,
        dict,
    ):
        raise ValueError(
            "Missing decision object."
        )

    expected = normalize_decision(
        decision_payload.get(
            "expected"
        )
    )

    actual = normalize_decision(
        decision_payload.get(
            "actual"
        )
    )

    validated = {
        "decision": {
            "expected": expected,
            "actual": actual,
            "correct": bool(
                decision_payload.get(
                    "correct",
                    False,
                )
            ),
            "reason": normalize_text(
                decision_payload.get(
                    "reason"
                )
            ),
        },
        "semantic": validate_dimension(
            payload,
            "semantic",
        ),
        "structural": validate_dimension(
            payload,
            "structural",
        ),
        "faithfulness": validate_dimension(
            payload,
            "faithfulness",
        ),
        "subtypes": {},
        "unsupported_claims": (
            payload.get(
                "unsupported_claims",
                [],
            )
            if isinstance(
                payload.get(
                    "unsupported_claims",
                    [],
                ),
                list,
            )
            else []
        ),
        "missing_required_content": (
            payload.get(
                "missing_required_content",
                [],
            )
            if isinstance(
                payload.get(
                    "missing_required_content",
                    [],
                ),
                list,
            )
            else []
        ),
        "overall_notes": normalize_text(
            payload.get(
                "overall_notes"
            )
        ),
    }

    for subtype in [
        "spatial",
        "numerical",
        "temporal",
        "topological",
        "categorical",
    ]:
        validated[
            "subtypes"
        ][subtype] = validate_subtype(
            payload,
            subtype,
        )

    # --------------------------------------------------------
    # Force applicability consistency with frozen gold.
    # Judge is not allowed to invent applicability.
    # --------------------------------------------------------

    subtype_to_key = {
        "spatial": "spatial",
        "numerical": "numerical",
        "temporal": "temporal",
        "topological": "topological",
        "categorical": "categorical",
    }

    for subtype, key in (
        subtype_to_key.items()
    ):
        expected = bool(
            expected_applicability.get(
                key,
                False,
            )
        )

        actual_subtype = (
            validated[
                "subtypes"
            ][subtype]
        )

        # For OOD-only samples, normal subtypes are not applicable
        # unless judge flags substantive unsupported claims.
        if (
            expected_applicability.get(
                "ood",
                False,
            )
            and not actual_subtype[
                "hallucination"
            ]
        ):
            expected = False

        if (
            not expected
            and actual_subtype[
                "applicable"
            ]
        ):
            # Convert to non-applicable rather than rewarding/penalizing
            # an out-of-scope subtype.
            actual_subtype[
                "applicable"
            ] = False
            actual_subtype[
                "score"
            ] = None

        elif (
            expected
            and not actual_subtype[
                "applicable"
            ]
        ):
            # Missing score for a required subtype is a judge schema failure.
            raise ValueError(
                f"Judge marked required subtype {subtype} not applicable."
            )

    return validated


# ============================================================
# SINGLE ITEM
# ============================================================

def judge_one(
    *,
    judge: OllamaJudge,
    gold: Dict[str, Any],
    generation: Dict[str, Any],
    source_path: Path,
    results_root: Path,
    output_root: Path,
) -> Dict[str, Any]:
    query_id = infer_query_id(
        generation,
        source_path,
    )

    model = infer_model(
        generation,
        source_path,
        results_root,
    )

    mode = infer_mode(
        generation,
        source_path,
        results_root,
    )

    generated_text = (
        extract_generated_text(
            generation
        )
    )

    decision = extract_decision(
        generation,
        generated_text,
    )

    retrieved_evidence = (
        extract_retrieved_evidence(
            generation
        )
    )

    deterministic = (
        deterministic_checks(
            gold,
            generated_text,
            decision,
        )
    )

    applicability = (
        gold_applicability(
            gold
        )
    )

    prompt = build_judge_prompt(
        gold=gold,
        generated_text=(
            generated_text
        ),
        decision=decision,
        retrieved_evidence=(
            retrieved_evidence
        ),
    )

    prompt_hash = sha256_text(
        prompt
    )

    item_dir = (
        output_root
        / sanitize_path_component(
            model
        )
        / sanitize_path_component(
            mode
        )
        / str(
            query_id
        )
    )

    ensure_dir(
        item_dir
    )

    prompt_path = (
        item_dir
        / "judge_prompt.txt"
    )

    prompt_path.write_text(
        prompt,
        encoding="utf-8",
    )

    raw_output = ""
    ollama_metadata: Dict[
        str,
        Any,
    ] = {}

    judge_status = "OK"
    judge_error = ""

    parsed: Optional[
        Dict[str, Any]
    ] = None

    validated: Optional[
        Dict[str, Any]
    ] = None

    try:
        raw_output, ollama_metadata = (
            judge.generate(
                prompt
            )
        )

        (
            item_dir
            / "judge_raw_output.txt"
        ).write_text(
            raw_output,
            encoding="utf-8",
        )

        parsed = parse_json_object(
            raw_output
        )

        validated = (
            validate_judge_payload(
                parsed,
                applicability,
            )
        )

        (
            item_dir
            / "judge_parsed.json"
        ).write_text(
            json.dumps(
                validated,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    except requests.Timeout as exc:
        judge_status = (
            "JUDGE_TIMEOUT"
        )

        judge_error = str(
            exc
        )

    except requests.RequestException as exc:
        judge_status = (
            "JUDGE_REQUEST_ERROR"
        )

        judge_error = str(
            exc
        )

    except Exception as exc:
        judge_status = (
            "JUDGE_PARSE_OR_SCHEMA_ERROR"
        )

        judge_error = (
            f"{type(exc).__name__}: "
            f"{exc}"
        )

    record = {
        "judge_script_version": (
            JUDGE_SCRIPT_VERSION
        ),
        "judge_prompt_version": (
            JUDGE_PROMPT_VERSION
        ),
        "query_id": query_id,
        "category": gold.get(
            "category",
            "",
        ),
        "query": gold.get(
            "query",
            "",
        ),
        "generator_model": model,
        "architecture_mode": mode,
        "source_generation_file": (
            str(
                source_path
            )
        ),
        "judge_model": (
            judge.model
        ),
        "judge_config": {
            "temperature": (
                judge.temperature
            ),
            "top_p": (
                judge.top_p
            ),
            "seed": (
                judge.seed
            ),
            "num_ctx": (
                judge.num_ctx
            ),
            "timeout_s": (
                judge.timeout
            ),
        },
        "judge_status": judge_status,
        "judge_error": (
            judge_error
        ),
        "judge_prompt_sha256": (
            prompt_hash
        ),
        "judge_raw_output_sha256": (
            sha256_text(
                raw_output
            )
            if raw_output
            else None
        ),
        "judge_ollama_metadata": (
            ollama_metadata
        ),
        "generated_decision": (
            decision
        ),
        "expected_decision": (
            normalize_decision(
                gold.get(
                    "expected_decision"
                )
            )
        ),
        "applicability": (
            applicability
        ),
        "deterministic_checks": (
            deterministic
        ),
        "scores": validated,
        "created_at": utc_now_iso(),
    }

    result_path = (
        item_dir
        / "judge_result.json"
    )

    result_path.write_text(
        json.dumps(
            record,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return record


def sanitize_path_component(
    value: str,
) -> str:
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
# AGGREGATION
# ============================================================

def score_if_valid(
    record: Dict[str, Any],
    dimension: str,
) -> Optional[float]:
    if (
        record.get(
            "judge_status"
        )
        != "OK"
    ):
        return None

    scores = record.get(
        "scores"
    )

    if not isinstance(
        scores,
        dict,
    ):
        return None

    item = scores.get(
        dimension
    )

    if not isinstance(
        item,
        dict,
    ):
        return None

    if not item.get(
        "applicable",
        False,
    ):
        return None

    value = item.get(
        "score"
    )

    if value is None:
        return None

    return float(
        value
    )


def subtype_score_if_valid(
    record: Dict[str, Any],
    subtype: str,
) -> Optional[float]:
    if (
        record.get(
            "judge_status"
        )
        != "OK"
    ):
        return None

    scores = record.get(
        "scores"
    )

    if not isinstance(
        scores,
        dict,
    ):
        return None

    subtypes = scores.get(
        "subtypes"
    )

    if not isinstance(
        subtypes,
        dict,
    ):
        return None

    item = subtypes.get(
        subtype
    )

    if not isinstance(
        item,
        dict,
    ):
        return None

    if not item.get(
        "applicable",
        False,
    ):
        return None

    value = item.get(
        "score"
    )

    if value is None:
        return None

    return float(
        value
    )


def subtype_hallucination(
    record: Dict[str, Any],
    subtype: str,
) -> Optional[bool]:
    if (
        record.get(
            "judge_status"
        )
        != "OK"
    ):
        return None

    scores = record.get(
        "scores"
    )

    if not isinstance(
        scores,
        dict,
    ):
        return None

    item = (
        scores
        .get(
            "subtypes",
            {},
        )
        .get(
            subtype
        )
    )

    if not isinstance(
        item,
        dict,
    ):
        return None

    return bool(
        item.get(
            "hallucination",
            False,
        )
    )


def summarize_group(
    records: Sequence[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:
    total = len(
        records
    )

    ok = [
        r
        for r in records
        if r.get(
            "judge_status"
        ) == "OK"
    ]

    decision_valid = [
        r
        for r in records
        if r.get(
            "deterministic_checks",
            {},
        ).get(
            "decision_valid",
            False,
        )
    ]

    decision_correct = [
        r
        for r in records
        if r.get(
            "deterministic_checks",
            {},
        ).get(
            "decision_correct",
            False,
        )
    ]

    summary: Dict[
        str,
        Any,
    ] = {
        "N": total,
        "judge_ok": len(
            ok
        ),
        "judge_error": (
            total
            - len(
                ok
            )
        ),
        "judge_coverage": (
            len(ok) / total
            if total
            else None
        ),
        "decision_valid_count": (
            len(
                decision_valid
            )
        ),
        "decision_correct_count": (
            len(
                decision_correct
            )
        ),
        "decision_accuracy": (
            len(
                decision_correct
            )
            / total
            if total
            else None
        ),
    }

    for dimension in [
        "semantic",
        "structural",
        "faithfulness",
    ]:
        values = [
            score
            for score in (
                score_if_valid(
                    r,
                    dimension,
                )
                for r in records
            )
            if score is not None
        ]

        summary[
            f"{dimension}_N"
        ] = len(
            values
        )

        summary[
            f"{dimension}_mean"
        ] = safe_mean(
            values
        )

        summary[
            f"{dimension}_std"
        ] = safe_stdev(
            values
        )

    for subtype in [
        "spatial",
        "numerical",
        "temporal",
        "topological",
        "categorical",
    ]:
        values = [
            score
            for score in (
                subtype_score_if_valid(
                    r,
                    subtype,
                )
                for r in records
            )
            if score is not None
        ]

        hall_flags = [
            flag
            for flag in (
                subtype_hallucination(
                    r,
                    subtype,
                )
                for r in records
            )
            if flag is not None
        ]

        summary[
            f"{subtype}_N"
        ] = len(
            values
        )

        summary[
            f"{subtype}_mean"
        ] = safe_mean(
            values
        )

        summary[
            f"{subtype}_std"
        ] = safe_stdev(
            values
        )

        summary[
            f"{subtype}_hallucination_count"
        ] = sum(
            1
            for flag in hall_flags
            if flag
        )

        summary[
            f"{subtype}_hallucination_rate"
        ] = (
            sum(
                1
                for flag in hall_flags
                if flag
            )
            / len(
                hall_flags
            )
            if hall_flags
            else None
        )

    return summary


def aggregate_records(
    records: Sequence[
        Dict[str, Any]
    ],
) -> Dict[str, Any]:
    by_model_mode: Dict[
        Tuple[str, str],
        List[
            Dict[str, Any]
        ],
    ] = defaultdict(list)

    by_category: Dict[
        str,
        List[
            Dict[str, Any]
        ],
    ] = defaultdict(list)

    for record in records:
        by_model_mode[
            (
                record.get(
                    "generator_model",
                    "unknown_model",
                ),
                record.get(
                    "architecture_mode",
                    "unknown_mode",
                ),
            )
        ].append(
            record
        )

        by_category[
            record.get(
                "category",
                "unknown",
            )
        ].append(
            record
        )

    return {
        "overall": (
            summarize_group(
                records
            )
        ),
        "by_model_mode": {
            f"{model}::{mode}": (
                summarize_group(
                    group
                )
            )
            for (
                model,
                mode,
            ), group in sorted(
                by_model_mode.items()
            )
        },
        "by_category": {
            category: (
                summarize_group(
                    group
                )
            )
            for (
                category,
                group,
            ) in sorted(
                by_category.items()
            )
        },
    }


# ============================================================
# CSV EXPORT
# ============================================================

def write_flat_csv(
    records: Sequence[
        Dict[str, Any]
    ],
    path: Path,
) -> None:
    import csv

    fields = [
        "query_id",
        "category",
        "generator_model",
        "architecture_mode",
        "judge_status",
        "expected_decision",
        "generated_decision",
        "decision_correct",
        "semantic_score",
        "structural_score",
        "faithfulness_score",
        "spatial_score",
        "spatial_hallucination",
        "numerical_score",
        "numerical_hallucination",
        "temporal_score",
        "temporal_hallucination",
        "topological_score",
        "topological_hallucination",
        "categorical_score",
        "categorical_hallucination",
        "judge_latency_s",
        "judge_prompt_sha256",
        "source_generation_file",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        for record in records:
            scores = (
                record.get(
                    "scores"
                )
                if isinstance(
                    record.get(
                        "scores"
                    ),
                    dict,
                )
                else {}
            )

            subtypes = (
                scores.get(
                    "subtypes",
                    {}
                )
                if isinstance(
                    scores,
                    dict,
                )
                else {}
            )

            def dim_score(
                name: str,
            ) -> Any:
                item = scores.get(
                    name,
                    {}
                )

                if not isinstance(
                    item,
                    dict,
                ):
                    return ""

                return (
                    item.get(
                        "score"
                    )
                    if item.get(
                        "applicable",
                        False,
                    )
                    else ""
                )

            def subtype_value(
                name: str,
                key: str,
            ) -> Any:
                item = subtypes.get(
                    name,
                    {}
                )

                if not isinstance(
                    item,
                    dict,
                ):
                    return ""

                if (
                    key == "score"
                    and not item.get(
                        "applicable",
                        False,
                    )
                ):
                    return ""

                return item.get(
                    key,
                    "",
                )

            writer.writerow({
                "query_id": record.get(
                    "query_id"
                ),
                "category": record.get(
                    "category"
                ),
                "generator_model": (
                    record.get(
                        "generator_model"
                    )
                ),
                "architecture_mode": (
                    record.get(
                        "architecture_mode"
                    )
                ),
                "judge_status": (
                    record.get(
                        "judge_status"
                    )
                ),
                "expected_decision": (
                    record.get(
                        "expected_decision"
                    )
                ),
                "generated_decision": (
                    record.get(
                        "generated_decision"
                    )
                ),
                "decision_correct": (
                    record.get(
                        "deterministic_checks",
                        {},
                    ).get(
                        "decision_correct"
                    )
                ),
                "semantic_score": (
                    dim_score(
                        "semantic"
                    )
                ),
                "structural_score": (
                    dim_score(
                        "structural"
                    )
                ),
                "faithfulness_score": (
                    dim_score(
                        "faithfulness"
                    )
                ),
                "spatial_score": (
                    subtype_value(
                        "spatial",
                        "score",
                    )
                ),
                "spatial_hallucination": (
                    subtype_value(
                        "spatial",
                        "hallucination",
                    )
                ),
                "numerical_score": (
                    subtype_value(
                        "numerical",
                        "score",
                    )
                ),
                "numerical_hallucination": (
                    subtype_value(
                        "numerical",
                        "hallucination",
                    )
                ),
                "temporal_score": (
                    subtype_value(
                        "temporal",
                        "score",
                    )
                ),
                "temporal_hallucination": (
                    subtype_value(
                        "temporal",
                        "hallucination",
                    )
                ),
                "topological_score": (
                    subtype_value(
                        "topological",
                        "score",
                    )
                ),
                "topological_hallucination": (
                    subtype_value(
                        "topological",
                        "hallucination",
                    )
                ),
                "categorical_score": (
                    subtype_value(
                        "categorical",
                        "score",
                    )
                ),
                "categorical_hallucination": (
                    subtype_value(
                        "categorical",
                        "hallucination",
                    )
                ),
                "judge_latency_s": (
                    record.get(
                        "judge_ollama_metadata",
                        {},
                    ).get(
                        "latency_s"
                    )
                ),
                "judge_prompt_sha256": (
                    record.get(
                        "judge_prompt_sha256"
                    )
                ),
                "source_generation_file": (
                    record.get(
                        "source_generation_file"
                    )
                ),
            })


# ============================================================
# OPTIONAL OLLAMA MODEL INFO
# ============================================================

def get_ollama_model_metadata(
    model: str,
) -> Dict[str, Any]:
    """
    Best-effort model metadata.
    Failure is recorded but does not block judging.
    """

    url = (
        OLLAMA_BASE_URL.rstrip("/")
        + "/api/show"
    )

    try:
        response = requests.post(
            url,
            json={
                "model": model,
            },
            timeout=30,
        )

        response.raise_for_status()

        body = response.json()

        return {
            "ok": True,
            "model": model,
            "details": body.get(
                "details"
            ),
            "model_info": body.get(
                "model_info"
            ),
            "parameters": body.get(
                "parameters"
            ),
            "template_sha256": (
                sha256_text(
                    body.get(
                        "template",
                        "",
                    )
                )
                if body.get(
                    "template"
                )
                else None
            ),
            "license": body.get(
                "license"
            ),
        }

    except Exception as exc:
        return {
            "ok": False,
            "model": model,
            "error": (
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
        }


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Judge HydroGraphRAG generation results "
            "against frozen ground truth."
        )
    )

    parser.add_argument(
        "--ground-truth",
        default=(
            DEFAULT_GROUND_TRUTH
        ),
    )

    parser.add_argument(
        "--results-root",
        default=(
            DEFAULT_RESULTS_ROOT
        ),
    )

    parser.add_argument(
        "--output-root",
        default=(
            DEFAULT_OUTPUT_ROOT
        ),
    )

    parser.add_argument(
        "--judge-model",
        default=(
            DEFAULT_JUDGE_MODEL
        ),
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=(
            DEFAULT_TEMPERATURE
        ),
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=DEFAULT_TOP_P,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
    )

    parser.add_argument(
        "--num-ctx",
        type=int,
        default=DEFAULT_NUM_CTX,
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
    )

    parser.add_argument(
        "--ids",
        nargs="*",
        default=None,
        help=(
            "Optional subset of query IDs "
            "for smoke testing."
        ),
    )

    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help=(
            "Optional generator model filter."
        ),
    )

    parser.add_argument(
        "--modes",
        nargs="*",
        default=None,
        help=(
            "Optional architecture mode filter."
        ),
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Re-run items even if "
            "judge_result.json exists."
        ),
    )

    args = parser.parse_args()

    gt_path = Path(
        args.ground_truth
    ).resolve()

    results_root = Path(
        args.results_root
    ).resolve()

    output_root = Path(
        args.output_root
    ).resolve()

    if not gt_path.is_file():
        raise FileNotFoundError(
            gt_path
        )

    if not results_root.is_dir():
        raise FileNotFoundError(
            results_root
        )

    ensure_dir(
        output_root
    )

    ground_truth, gt_by_id = (
        load_ground_truth(
            gt_path
        )
    )

    generation_files = (
        discover_generation_files(
            results_root
        )
    )

    id_filter = (
        {
            str(v)
            for v in args.ids
        }
        if args.ids
        else None
    )

    model_filter = (
        {
            normalize_text(v)
            for v in args.models
        }
        if args.models
        else None
    )

    mode_filter = (
        {
            normalize_text(v)
            for v in args.modes
        }
        if args.modes
        else None
    )

    selected_files = []

    for path in (
        generation_files
    ):
        try:
            generation = (
                read_generation_result(
                    path
                )
            )
        except Exception:
            continue

        query_id = infer_query_id(
            generation,
            path,
        )

        if (
            id_filter is not None
            and query_id not in id_filter
        ):
            continue

        model = infer_model(
            generation,
            path,
            results_root,
        )

        mode = infer_mode(
            generation,
            path,
            results_root,
        )

        if (
            model_filter is not None
            and model not in model_filter
        ):
            continue

        if (
            mode_filter is not None
            and mode not in mode_filter
        ):
            continue

        selected_files.append(
            path
        )

    print("=" * 72)
    print("HydroGraphRAG Final Judge")
    print("=" * 72)
    print(f"Ground truth: {gt_path}")
    print(
        "Ground-truth SHA256: "
        + sha256_file(
            gt_path
        )
    )
    print(
        f"Ground-truth items: "
        f"{len(ground_truth)}"
    )
    print(
        f"Generation files discovered: "
        f"{len(generation_files)}"
    )
    print(
        f"Selected for judging: "
        f"{len(selected_files)}"
    )
    print(
        f"Judge model: "
        f"{args.judge_model}"
    )
    print("")

    if not selected_files:
        raise RuntimeError(
            "No generation result files selected."
        )

    judge = OllamaJudge(
        model=args.judge_model,
        temperature=args.temperature,
        top_p=args.top_p,
        seed=args.seed,
        num_ctx=args.num_ctx,
        timeout=args.timeout,
    )

    judge_model_metadata = (
        get_ollama_model_metadata(
            args.judge_model
        )
    )

    manifest = {
        "judge_script_version": (
            JUDGE_SCRIPT_VERSION
        ),
        "judge_prompt_version": (
            JUDGE_PROMPT_VERSION
        ),
        "created_at": utc_now_iso(),
        "ground_truth_path": (
            str(
                gt_path
            )
        ),
        "ground_truth_sha256": (
            sha256_file(
                gt_path
            )
        ),
        "results_root": (
            str(
                results_root
            )
        ),
        "output_root": (
            str(
                output_root
            )
        ),
        "judge_model": (
            args.judge_model
        ),
        "judge_model_metadata": (
            judge_model_metadata
        ),
        "judge_config": {
            "temperature": (
                args.temperature
            ),
            "top_p": args.top_p,
            "seed": args.seed,
            "num_ctx": (
                args.num_ctx
            ),
            "timeout_s": (
                args.timeout
            ),
        },
        "selected_generation_files": (
            len(
                selected_files
            )
        ),
        "filters": {
            "ids": args.ids,
            "models": args.models,
            "modes": args.modes,
        },
        "policy": {
            "empty_gold_is_not_perfect_score": True,
            "non_applicable_score_is_null": True,
            "judge_failure_is_not_score": True,
            "ood_separate_from_faithfulness": True,
            "expected_missing_facts_enforced": True,
            "architecture_label_hidden_from_prompt": True,
            "human_evaluation": False,
        },
    }

    (
        output_root
        / "judge_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    records = []

    for index, path in enumerate(
        selected_files,
        start=1,
    ):
        generation = (
            read_generation_result(
                path
            )
        )

        query_id = infer_query_id(
            generation,
            path,
        )

        model = infer_model(
            generation,
            path,
            results_root,
        )

        mode = infer_mode(
            generation,
            path,
            results_root,
        )

        print(
            f"[{index}/{len(selected_files)}] "
            f"id={query_id} "
            f"model={model} "
            f"mode={mode}"
        )

        gold = gt_by_id.get(
            query_id
        )

        if gold is None:
            record = {
                "query_id": query_id,
                "generator_model": model,
                "architecture_mode": mode,
                "source_generation_file": (
                    str(path)
                ),
                "judge_status": (
                    "GROUND_TRUTH_NOT_FOUND"
                ),
                "judge_error": (
                    f"No frozen gold for query id "
                    f"{query_id}."
                ),
            }

            records.append(
                record
            )
            continue

        item_dir = (
            output_root
            / sanitize_path_component(
                model
            )
            / sanitize_path_component(
                mode
            )
            / str(
                query_id
            )
        )

        cached_result = (
            item_dir
            / "judge_result.json"
        )

        if (
            cached_result.is_file()
            and not args.overwrite
        ):
            try:
                with cached_result.open(
                    "r",
                    encoding="utf-8",
                ) as f:
                    cached = json.load(f)

                # Only reuse if prompt/script versions and frozen GT hash
                # remain compatible.
                if (
                    cached.get(
                        "judge_script_version"
                    )
                    == JUDGE_SCRIPT_VERSION
                    and cached.get(
                        "judge_prompt_version"
                    )
                    == JUDGE_PROMPT_VERSION
                ):
                    records.append(
                        cached
                    )

                    print(
                        "  -> cached"
                    )

                    continue
            except Exception:
                pass

        record = judge_one(
            judge=judge,
            gold=gold,
            generation=generation,
            source_path=path,
            results_root=results_root,
            output_root=output_root,
        )

        records.append(
            record
        )

        print(
            "  -> "
            + record.get(
                "judge_status",
                "UNKNOWN",
            )
        )

    # --------------------------------------------------------
    # Final outputs
    # --------------------------------------------------------

    all_results_path = (
        output_root
        / "judge_results.json"
    )

    all_results_path.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = aggregate_records(
        records
    )

    summary[
        "judge_script_version"
    ] = JUDGE_SCRIPT_VERSION

    summary[
        "judge_prompt_version"
    ] = JUDGE_PROMPT_VERSION

    summary[
        "ground_truth_sha256"
    ] = sha256_file(
        gt_path
    )

    summary[
        "created_at"
    ] = utc_now_iso()

    summary_path = (
        output_root
        / "judge_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    csv_path = (
        output_root
        / "judge_results.csv"
    )

    write_flat_csv(
        records,
        csv_path,
    )

    print("")
    print("=" * 72)
    print("COMPLETE")
    print("=" * 72)
    print(
        f"Judge results: {all_results_path}"
    )
    print(
        f"Summary:       {summary_path}"
    )
    print(
        f"CSV:           {csv_path}"
    )
    print(
        "Manifest:      "
        + str(
            output_root
            / "judge_manifest.json"
        )
    )

    overall = summary.get(
        "overall",
        {},
    )

    print("")
    print(
        "Judge coverage: "
        f"{overall.get('judge_ok', 0)}/"
        f"{overall.get('N', 0)}"
    )

    print(
        "Decision accuracy: "
        f"{overall.get('decision_accuracy')}"
    )

    print(
        "Faithfulness mean: "
        f"{overall.get('faithfulness_mean')}"
    )


if __name__ == "__main__":
    main()