import ast
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from tqdm import tqdm

from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from planner.generator import SolutionPlanner


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ============================================================
# PATHS
# ============================================================

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))

GROUND_TRUTH_PATH = os.path.join(
    EVAL_DIR,
    "ground_truth.json",
)

GENERATION_OUTPUT_PATH = os.path.join(
    EVAL_DIR,
    "generation_results.json",
)

RESULTS_DIR = os.path.join(
    EVAL_DIR,
    "results",
)

EXPERIMENT_MANIFEST_PATH = os.path.join(
    EVAL_DIR,
    "experiment_manifest.json",
)

DATA_DIR = os.path.join(
    EVAL_DIR,
    "data",
)


# ============================================================
# REPRODUCIBILITY CONFIGURATION
# ============================================================

GENERATION_CONFIG = {
    "temperature": 0.0,
    "top_p": 1.0,
    "seed": 42,
    "context_size": 8192,
}

EXECUTION_TIMEOUT_SECONDS = 30

VECTOR_TOP_K = 5

# IMPORTANT:
# This runner currently implements an exact final-prompt response cache.
# It is deliberately NOT called a semantic cache.
#
# A separate semantic-cache study should use embeddings + a fixed
# similarity threshold and should be reported separately from the
# frozen benchmark.
CACHE_IMPLEMENTATION = "exact_prompt_response_cache"


# ============================================================
# GENERATOR MODELS
# ============================================================

GENERATOR_MODELS = [
    "qwen2.5-coder:7b",
    "qwen2.5-coder:32b",
    "llama3.1:8b",
    "gemma2:27b",
    "codestral",
    "mistral-nemo",
    "gemma4:31b",
]


# ============================================================
# ABLATION STUDY
# ============================================================

ABLATION_MODES = {
    "Baseline": {
        "type": "baseline",
        "use_cda": False,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    "VectorRAG": {
        "type": "vector_rag",
        "use_cda": False,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    "HydroGraphRAG": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_CDA": {
        "type": "hydrographrag",
        "use_cda": False,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_WKT": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_Template": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": False,
        "use_cache": True,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_OOD": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": False,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_Cache": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    "HydroGraphRAG_no_Sandbox": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": False,
    },
}


# ============================================================
# FAILURE TYPES
# ============================================================

FAILURE_NONE = "NONE"
FAILURE_CDA = "CDA_ERROR"
FAILURE_RETRIEVAL = "RETRIEVAL_ERROR"
FAILURE_GENERATION = "GENERATION_ERROR"
FAILURE_INVALID_DECISION = "INVALID_DECISION"
FAILURE_SYNTAX = "SYNTAX_ERROR"
FAILURE_EXECUTION = "EXECUTION_ERROR"
FAILURE_TIMEOUT = "EXECUTION_TIMEOUT"


# ============================================================
# EXECUTION STATUSES
# ============================================================

EXEC_NOT_REQUESTED = "NOT_REQUESTED"
EXEC_SUCCESS = "SUCCESS"
EXEC_ERROR = "EXECUTION_ERROR"
EXEC_TIMEOUT = "TIMEOUT"
EXEC_SKIPPED_ABSTAIN = "SKIPPED_ABSTAIN"
EXEC_SKIPPED_INVALID = "SKIPPED_INVALID_DECISION"
EXEC_SKIPPED_SYNTAX = "SKIPPED_SYNTAX_ERROR"
EXEC_SKIPPED_GENERATION_ERROR = "SKIPPED_GENERATION_ERROR"


# ============================================================
# PIPELINE
# ============================================================

class GenerationPipeline:

    def __init__(self):
        logging.info(
            "⏳ Инициализация среды тестирования..."
        )

        self.db = HydroDatabase()
        self.embedder = EmbeddingsManager()

        # Exact final-prompt response cache.
        #
        # Key:
        #   sha256(final_prompt)
        #
        # Value:
        #   raw model response
        #
        # This is intentionally not labelled "semantic cache".
        self.response_cache: Dict[str, str] = {}

        self.run_id = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def normalize_entity(text: Any) -> str:
        if text is None:
            return ""

        value = str(text).strip().lower()

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value

    @staticmethod
    def safe_name(text: Any) -> str:
        value = str(text)

        value = re.sub(
            r"[^A-Za-z0-9._-]+",
            "_",
            value,
        )

        value = value.strip("._")

        return value or "unknown"

    @staticmethod
    def sha256_text(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    # ========================================================
    # JSON / TEXT ARTIFACT HELPERS
    # ========================================================

    @staticmethod
    def write_text(
        path: str,
        content: Any,
    ) -> None:
        os.makedirs(
            os.path.dirname(path),
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                "" if content is None else str(content)
            )

    @staticmethod
    def write_json(
        path: str,
        content: Any,
    ) -> None:
        os.makedirs(
            os.path.dirname(path),
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                content,
                f,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

    # ========================================================
    # CODE EXTRACTION
    # ========================================================

    def extract_python_code(
        self,
        text: Any,
    ) -> str:
        """
        Extracts only the implementation code from the model response.

        Preferred format:
            ### Implementation Code:
            ```python
            ...
            ```

        Fallback:
            first fenced Python block.
        """

        if not text:
            return ""

        text = str(text)

        implementation_match = re.search(
            r"###\s*Implementation\s+Code\s*:\s*"
            r"```python\s*(.*?)```",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if implementation_match:
            return implementation_match.group(1).strip()

        python_match = re.search(
            r"```python\s*(.*?)```",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if python_match:
            return python_match.group(1).strip()

        generic_match = re.search(
            r"```\s*(.*?)```",
            text,
            flags=re.DOTALL,
        )

        if generic_match:
            return generic_match.group(1).strip()

        # Do not treat the entire structured response as Python.
        return ""

    # ========================================================
    # DECISION EXTRACTION
    # ========================================================

    @staticmethod
    def extract_decision(
        text: Any,
    ) -> Tuple[str, bool, Optional[str]]:
        """
        Valid decisions:
            ANSWER
            ABSTAIN

        Missing or malformed decision:
            INVALID
        """

        if not text:
            return (
                "INVALID",
                False,
                None,
            )

        text = str(text)

        decision_match = re.search(
            r"^\s*decision\s*:\s*(ANSWER|ABSTAIN)\s*$",
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        if not decision_match:
            return (
                "INVALID",
                False,
                None,
            )

        decision = (
            decision_match
            .group(1)
            .upper()
        )

        reason_match = re.search(
            r"^\s*abstain_reason\s*:\s*(.*?)\s*$",
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        reason = (
            reason_match.group(1).strip()
            if reason_match
            else None
        )

        if (
            reason is not None
            and reason.upper() == "NONE"
        ):
            reason = None

        if (
            decision == "ABSTAIN"
            and not reason
        ):
            # Decision exists, but contract is incomplete.
            return (
                "INVALID",
                False,
                None,
            )

        return (
            decision,
            True,
            reason,
        )

    # ========================================================
    # SYNTAX CHECK
    # ========================================================

    @staticmethod
    def check_syntax(
        code_str: str,
    ) -> bool:
        if not code_str:
            return False

        try:
            ast.parse(
                code_str
            )
            return True

        except SyntaxError:
            return False

        except Exception:
            return False

    # ========================================================
    # RELATION HELPERS
    # ========================================================

    @staticmethod
    def relation_local_name(
        relation: Any,
    ) -> str:
        value = str(
            relation or ""
        ).strip()

        value = value.strip("<>")

        if "#" in value:
            value = value.rsplit(
                "#",
                1,
            )[-1]

        elif "/" in value:
            value = value.rsplit(
                "/",
                1,
            )[-1]

        if ":" in value:
            value = value.rsplit(
                ":",
                1,
            )[-1]

        return value.strip().lower()

    def is_wkt_triple(
        self,
        triple: Dict[str, Any],
    ) -> bool:
        relation = triple.get(
            "rel",
            triple.get(
                "relation",
                triple.get(
                    "predicate",
                    "",
                ),
            ),
        )

        return (
            self.relation_local_name(
                relation
            )
            in {
                "aswkt",
                "haswkt",
            }
        )

    # ========================================================
    # VECTOR RETRIEVAL
    # ========================================================

    def get_vector_context(
        self,
        query: str,
        retriever: GraphRetriever,
        k: int = VECTOR_TOP_K,
    ) -> Tuple[str, List[str], Optional[str]]:
        """
        Real flat vector retrieval.

        Returns:
            context_string
            retrieved_entity_names
            error_message
        """

        try:
            candidates = (
                retriever._get_all_entities()
            )

            scored = (
                self.embedder.find_top_matches(
                    query,
                    candidates,
                    top_k=k,
                )
            )

            entities: List[str] = []
            context_lines: List[str] = []

            for item in scored:
                if not item:
                    continue

                entity = item[0]

                if not isinstance(
                    entity,
                    dict,
                ):
                    continue

                entity_name = str(
                    entity.get(
                        "name",
                        "",
                    )
                ).strip()

                if not entity_name:
                    continue

                entities.append(
                    entity_name
                )

                context_lines.append(
                    (
                        f"Entity: {entity_name} "
                        f"(Type: "
                        f"{entity.get('category', 'Unknown')})"
                    )
                )

            return (
                "\n".join(
                    context_lines
                ),
                entities,
                None,
            )

        except Exception as exc:
            error = str(exc)

            logging.warning(
                "VectorRAG retrieval error: %s",
                error,
            )

            return (
                "",
                [],
                error,
            )

    # ========================================================
    # GRAPH ENTITY EXTRACTION
    # ========================================================

    @staticmethod
    def looks_like_wkt(
        value: Any,
    ) -> bool:
        text = str(
            value or ""
        ).strip().upper()

        return text.startswith(
            (
                "POINT",
                "LINESTRING",
                "POLYGON",
                "MULTIPOINT",
                "MULTILINESTRING",
                "MULTIPOLYGON",
                "GEOMETRYCOLLECTION",
            )
        )

    @staticmethod
    def looks_like_numeric_literal(
        value: Any,
    ) -> bool:
        text = str(
            value or ""
        ).strip()

        return bool(
            re.fullmatch(
                r"[-+]?\d+(?:[.,]\d+)?"
                r"(?:\s*[A-Za-zА-Яа-я/%³²]+)?",
                text,
            )
        )

    @staticmethod
    def looks_like_date_literal(
        value: Any,
    ) -> bool:
        text = str(
            value or ""
        ).strip()

        return bool(
            re.fullmatch(
                r"\d{4}(?:-\d{1,2}(?:-\d{1,2})?)?",
                text,
            )
        )

    def extract_entities_from_triples(
        self,
        triples: Any,
    ) -> List[str]:
        """
        Best-effort entity extraction from flattened graph triples.

        Literal-looking WKT/numeric/date targets are excluded.

        The actual retrieved graph is still preserved separately in
        retrieval_context for later triple-level evaluation.
        """

        if not isinstance(
            triples,
            list,
        ):
            return []

        entities: Dict[str, str] = {}

        for triple in triples:
            if not isinstance(
                triple,
                dict,
            ):
                continue

            source = triple.get(
                "from",
                triple.get(
                    "source",
                    "",
                ),
            )

            target = triple.get(
                "to",
                triple.get(
                    "target",
                    "",
                ),
            )

            for node in (
                source,
                target,
            ):
                text = str(
                    node or ""
                ).strip()

                if not text:
                    continue

                if self.looks_like_wkt(
                    text
                ):
                    continue

                if self.looks_like_numeric_literal(
                    text
                ):
                    continue

                if self.looks_like_date_literal(
                    text
                ):
                    continue

                normalized = (
                    self.normalize_entity(
                        text
                    )
                )

                if len(
                    normalized
                ) <= 1:
                    continue

                entities.setdefault(
                    normalized,
                    text,
                )

        return list(
            entities.values()
        )

    # ========================================================
    # RETRIEVAL METRICS
    # ========================================================

    def calculate_retrieval_metrics(
        self,
        retrieved_entities_list: Any,
        expected_entities: Any,
        triples_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Entity-level Precision / Recall / F1.

        IMPORTANT:
        Numerator and denominator are both entity-level.
        """

        expected_entities = (
            expected_entities
            if isinstance(
                expected_entities,
                list,
            )
            else []
        )

        retrieved_entities_list = (
            retrieved_entities_list
            if isinstance(
                retrieved_entities_list,
                list,
            )
            else []
        )

        truth_nodes = {
            self.normalize_entity(
                entity
            )
            for entity in expected_entities
            if str(
                entity
            ).strip()
        }

        retrieved_nodes = {
            self.normalize_entity(
                entity
            )
            for entity in retrieved_entities_list
            if str(
                entity
            ).strip()
        }

        matched = (
            truth_nodes
            & retrieved_nodes
        )

        true_positive = len(
            matched
        )

        retrieved_count = len(
            retrieved_nodes
        )

        expected_count = len(
            truth_nodes
        )

        if (
            expected_count == 0
            and retrieved_count == 0
        ):
            precision = 1.0
            recall = 1.0
            f1 = 1.0

        elif expected_count == 0:
            precision = 0.0
            recall = 0.0
            f1 = 0.0

        else:
            precision = (
                true_positive
                / retrieved_count
                if retrieved_count > 0
                else 0.0
            )

            recall = (
                true_positive
                / expected_count
            )

            f1 = (
                2
                * precision
                * recall
                / (
                    precision
                    + recall
                )
                if (
                    precision
                    + recall
                ) > 0
                else 0.0
            )

        return {
            "precision": round(
                precision,
                4,
            ),
            "recall": round(
                recall,
                4,
            ),
            "f1": round(
                f1,
                4,
            ),
            "targets_found": (
                true_positive
            ),
            "retrieved_entities": (
                retrieved_count
            ),
            "retrieved_triples": int(
                triples_count
            ),
            "matched_entities": sorted(
                matched
            ),
        }

    # ========================================================
    # CDA
    # ========================================================

    def build_demand(
        self,
        query: str,
        identifier: DemandIdentifier,
        use_cda: bool,
        use_ood: bool,
    ) -> Tuple[Dict[str, Any], float, Optional[str]]:
        """
        Returns:
            demand
            cda_latency
            cda_error

        For no_OOD ablation:
        if CDA classifies the query as anomalous, the category is
        overridden before GraphRetriever is called. This prevents the
        retriever's own anomalous-query early return from accidentally
        preserving OOD rejection in the no_OOD ablation.
        """

        if not use_cda:
            return (
                {
                    "category": "explicit",
                    "extracted_inputs": [
                        query
                    ],
                    "target_output": "unknown",
                    "modeling_logic": (
                        "direct retrieval"
                    ),
                },
                0.0,
                None,
            )

        start = time.perf_counter()

        try:
            demand = (
                identifier.analyze_query(
                    query
                )
            )

            latency = round(
                time.perf_counter()
                - start,
                4,
            )

            if not isinstance(
                demand,
                dict,
            ):
                raise ValueError(
                    "CDA returned a non-dict result."
                )

            category = str(
                demand.get(
                    "category",
                    "",
                )
            ).strip().lower()

            if (
                category
                in {
                    "",
                    "error",
                }
            ):
                raise ValueError(
                    (
                        "CDA returned invalid "
                        f"category: {category!r}"
                    )
                )

            demand = dict(
                demand
            )

            demand[
                "original_category"
            ] = category

            # Critical for the no_OOD ablation.
            if (
                not use_ood
                and category == "anomalous"
            ):
                demand[
                    "category"
                ] = "explicit"

                demand[
                    "ood_override_applied"
                ] = True

            else:
                demand[
                    "ood_override_applied"
                ] = False

            return (
                demand,
                latency,
                None,
            )

        except Exception as exc:
            latency = round(
                time.perf_counter()
                - start,
                4,
            )

            error = str(
                exc
            )

            logging.warning(
                "CDA error: %s",
                error,
            )

            return (
                {
                    "category": "explicit",
                    "extracted_inputs": [
                        query
                    ],
                    "target_output": "unknown",
                    "modeling_logic": (
                        "CDA fallback after error"
                    ),
                    "original_category": (
                        "error"
                    ),
                    "ood_override_applied": False,
                },
                latency,
                error,
            )

    # ========================================================
    # RETRIEVAL
    # ========================================================

    def perform_retrieval(
        self,
        query: str,
        config: Dict[str, Any],
        identifier: DemandIdentifier,
        retriever: GraphRetriever,
    ) -> Dict[str, Any]:
        """
        Runs the retrieval stage for one architecture.

        Every architecture measures its own retrieval/CDA work,
        so total latency is not contaminated by precomputed shared work.
        """

        method_type = config[
            "type"
        ]

        cda_latency = 0.0
        retrieval_latency = 0.0

        cda_error = None
        retrieval_error = None

        demand: Optional[
            Dict[str, Any]
        ] = None

        context_data: Any = []
        retrieved_entities: List[str] = []
        triples_count = 0

        # ----------------------------------------------------
        # BASELINE
        # ----------------------------------------------------

        if method_type == "baseline":
            return {
                "demand": None,
                "context_data": [],
                "retrieved_entities": [],
                "retrieved_triples": 0,
                "cda_latency": 0.0,
                "retrieval_latency": 0.0,
                "cda_error": None,
                "retrieval_error": None,
            }

        # ----------------------------------------------------
        # VECTOR RAG
        # ----------------------------------------------------

        if method_type == "vector_rag":
            retrieval_start = (
                time.perf_counter()
            )

            (
                context_string,
                vector_entities,
                retrieval_error,
            ) = self.get_vector_context(
                query=query,
                retriever=retriever,
                k=VECTOR_TOP_K,
            )

            retrieval_latency = round(
                time.perf_counter()
                - retrieval_start,
                4,
            )

            return {
                "demand": None,
                "context_data": (
                    context_string
                ),
                "retrieved_entities": (
                    vector_entities
                ),
                "retrieved_triples": 0,
                "cda_latency": 0.0,
                "retrieval_latency": (
                    retrieval_latency
                ),
                "cda_error": None,
                "retrieval_error": (
                    retrieval_error
                ),
            }

        # ----------------------------------------------------
        # HYDROGRAPH RAG
        # ----------------------------------------------------

        (
            demand,
            cda_latency,
            cda_error,
        ) = self.build_demand(
            query=query,
            identifier=identifier,
            use_cda=config[
                "use_cda"
            ],
            use_ood=config[
                "use_ood"
            ],
        )

        retrieval_start = (
            time.perf_counter()
        )

        try:
            raw_triples = (
                retriever.find_solution_subgraph(
                    demand
                )
            )

            if not isinstance(
                raw_triples,
                list,
            ):
                raw_triples = []

        except Exception as exc:
            retrieval_error = str(
                exc
            )

            logging.warning(
                (
                    "Graph retrieval error | "
                    "query=%s | error=%s"
                ),
                query,
                retrieval_error,
            )

            raw_triples = []

        if config[
            "use_wkt"
        ]:
            context_data = (
                raw_triples
            )

        else:
            context_data = [
                triple
                for triple
                in raw_triples
                if (
                    isinstance(
                        triple,
                        dict,
                    )
                    and not self.is_wkt_triple(
                        triple
                    )
                )
            ]

        retrieved_entities = (
            self.extract_entities_from_triples(
                context_data
            )
        )

        triples_count = len(
            context_data
        )

        retrieval_latency = round(
            time.perf_counter()
            - retrieval_start,
            4,
        )

        return {
            "demand": demand,
            "context_data": (
                context_data
            ),
            "retrieved_entities": (
                retrieved_entities
            ),
            "retrieved_triples": (
                triples_count
            ),
            "cda_latency": (
                cda_latency
            ),
            "retrieval_latency": (
                retrieval_latency
            ),
            "cda_error": (
                cda_error
            ),
            "retrieval_error": (
                retrieval_error
            ),
        }

    # ========================================================
    # EXECUTION
    # ========================================================

    def execute_code(
        self,
        code_str: str,
        output_html_name: str,
        use_sandbox: bool,
        artifact_dir: str,
    ) -> Dict[str, Any]:
        """
        Executes generated Python.

        Same timeout for sandbox / no-sandbox.

        Sandbox:
            temporary working directory
            copied evaluation/data folder

        No-sandbox ablation:
            direct host execution in EVAL_DIR

        Persistent artifacts are copied to artifact_dir before any
        temporary directory is removed.
        """

        result_payload = {
            "success": False,
            "status": EXEC_NOT_REQUESTED,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "has_html": False,
            "timeout": False,
            "latency": 0.0,
        }

        if not code_str:
            result_payload[
                "status"
            ] = EXEC_SKIPPED_SYNTAX

            result_payload[
                "stderr"
            ] = "No executable code."

            return result_payload

        start = time.perf_counter()

        # ----------------------------------------------------
        # SANDBOX MODE
        # ----------------------------------------------------

        if use_sandbox:
            try:
                with tempfile.TemporaryDirectory(
                    prefix="hydro_eval_"
                ) as local_sandbox:

                    script_path = os.path.join(
                        local_sandbox,
                        "script.py",
                    )

                    with open(
                        script_path,
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(
                            code_str
                        )

                    sandbox_data = os.path.join(
                        local_sandbox,
                        "data",
                    )

                    if os.path.isdir(
                        DATA_DIR
                    ):
                        shutil.copytree(
                            DATA_DIR,
                            sandbox_data,
                        )

                    completed = subprocess.run(
                        [
                            sys.executable,
                            "script.py",
                        ],
                        cwd=local_sandbox,
                        capture_output=True,
                        text=True,
                        timeout=(
                            EXECUTION_TIMEOUT_SECONDS
                        ),
                    )

                    html_path = os.path.join(
                        local_sandbox,
                        output_html_name,
                    )

                    has_html = os.path.isfile(
                        html_path
                    )

                    if has_html:
                        shutil.copy2(
                            html_path,
                            os.path.join(
                                artifact_dir,
                                "map.html",
                            ),
                        )

                    result_payload.update(
                        {
                            "success": (
                                completed.returncode
                                == 0
                            ),
                            "status": (
                                EXEC_SUCCESS
                                if completed.returncode
                                == 0
                                else EXEC_ERROR
                            ),
                            "returncode": (
                                completed.returncode
                            ),
                            "stdout": (
                                completed.stdout
                                or ""
                            ),
                            "stderr": (
                                completed.stderr
                                or ""
                            ),
                            "has_html": (
                                has_html
                            ),
                        }
                    )

            except subprocess.TimeoutExpired as exc:
                result_payload.update(
                    {
                        "success": False,
                        "status": (
                            EXEC_TIMEOUT
                        ),
                        "returncode": None,
                        "stdout": (
                            exc.stdout
                            if isinstance(
                                exc.stdout,
                                str,
                            )
                            else ""
                        ),
                        "stderr": (
                            exc.stderr
                            if isinstance(
                                exc.stderr,
                                str,
                            )
                            else (
                                "Execution timeout "
                                f"({EXECUTION_TIMEOUT_SECONDS}s)"
                            )
                        ),
                        "has_html": False,
                        "timeout": True,
                    }
                )

            except Exception as exc:
                result_payload.update(
                    {
                        "success": False,
                        "status": (
                            EXEC_ERROR
                        ),
                        "stderr": str(
                            exc
                        ),
                        "has_html": False,
                    }
                )

        # ----------------------------------------------------
        # NO-SANDBOX MODE
        # ----------------------------------------------------

        else:
            temp_script_name = (
                "unsafe_script_"
                f"{os.getpid()}_"
                f"{time.time_ns()}.py"
            )

            temp_script_path = (
                os.path.join(
                    EVAL_DIR,
                    temp_script_name,
                )
            )

            host_html_path = (
                os.path.join(
                    EVAL_DIR,
                    output_html_name,
                )
            )

            try:
                # Prevent a stale map from being counted.
                if os.path.exists(
                    host_html_path
                ):
                    os.remove(
                        host_html_path
                    )

                with open(
                    temp_script_path,
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(
                        code_str
                    )

                completed = subprocess.run(
                    [
                        sys.executable,
                        temp_script_name,
                    ],
                    cwd=EVAL_DIR,
                    capture_output=True,
                    text=True,
                    timeout=(
                        EXECUTION_TIMEOUT_SECONDS
                    ),
                )

                has_html = os.path.isfile(
                    host_html_path
                )

                if has_html:
                    shutil.copy2(
                        host_html_path,
                        os.path.join(
                            artifact_dir,
                            "map.html",
                        ),
                    )

                result_payload.update(
                    {
                        "success": (
                            completed.returncode
                            == 0
                        ),
                        "status": (
                            EXEC_SUCCESS
                            if completed.returncode
                            == 0
                            else EXEC_ERROR
                        ),
                        "returncode": (
                            completed.returncode
                        ),
                        "stdout": (
                            completed.stdout
                            or ""
                        ),
                        "stderr": (
                            completed.stderr
                            or ""
                        ),
                        "has_html": (
                            has_html
                        ),
                    }
                )

            except subprocess.TimeoutExpired as exc:
                result_payload.update(
                    {
                        "success": False,
                        "status": (
                            EXEC_TIMEOUT
                        ),
                        "returncode": None,
                        "stdout": (
                            exc.stdout
                            if isinstance(
                                exc.stdout,
                                str,
                            )
                            else ""
                        ),
                        "stderr": (
                            exc.stderr
                            if isinstance(
                                exc.stderr,
                                str,
                            )
                            else (
                                "Execution timeout "
                                f"({EXECUTION_TIMEOUT_SECONDS}s)"
                            )
                        ),
                        "has_html": False,
                        "timeout": True,
                    }
                )

            except Exception as exc:
                result_payload.update(
                    {
                        "success": False,
                        "status": (
                            EXEC_ERROR
                        ),
                        "stderr": str(
                            exc
                        ),
                        "has_html": False,
                    }
                )

            finally:
                if os.path.exists(
                    temp_script_path
                ):
                    try:
                        os.remove(
                            temp_script_path
                        )
                    except OSError:
                        logging.warning(
                            "Could not remove %s",
                            temp_script_path,
                        )

                if os.path.exists(
                    host_html_path
                ):
                    try:
                        os.remove(
                            host_html_path
                        )
                    except OSError:
                        logging.warning(
                            "Could not remove %s",
                            host_html_path,
                        )

        result_payload[
            "latency"
        ] = round(
            time.perf_counter()
            - start,
            4,
        )

        return result_payload

    # ========================================================
    # ARTIFACT DIRECTORY
    # ========================================================

    def prepare_artifact_dir(
        self,
        model_name: str,
        mode_name: str,
        query_id: str,
    ) -> str:
        path = os.path.join(
            RESULTS_DIR,
            self.safe_name(
                model_name
            ),
            self.safe_name(
                mode_name
            ),
            self.safe_name(
                query_id
            ),
        )

        if os.path.exists(
            path
        ):
            shutil.rmtree(
                path
            )

        os.makedirs(
            path,
            exist_ok=True,
        )

        return path

    # ========================================================
    # ARCHITECTURE RUN
    # ========================================================

    def run_architecture(
        self,
        model_name: str,
        query: str,
        query_id: str,
        category: str,
        expected_entities: List[str],
        mode_name: str,
        config: Dict[str, Any],
        identifier: DemandIdentifier,
        retriever: GraphRetriever,
        planner: SolutionPlanner,
    ) -> Dict[str, Any]:

        architecture_start = (
            time.perf_counter()
        )

        artifact_dir = (
            self.prepare_artifact_dir(
                model_name=model_name,
                mode_name=mode_name,
                query_id=query_id,
            )
        )

        # ----------------------------------------------------
        # RETRIEVAL
        # ----------------------------------------------------

        retrieval_result = (
            self.perform_retrieval(
                query=query,
                config=config,
                identifier=identifier,
                retriever=retriever,
            )
        )

        context_data = (
            retrieval_result[
                "context_data"
            ]
        )

        retrieved_entities = (
            retrieval_result[
                "retrieved_entities"
            ]
        )

        triples_count = int(
            retrieval_result[
                "retrieved_triples"
            ]
        )

        cda_latency = float(
            retrieval_result[
                "cda_latency"
            ]
        )

        retrieval_latency = float(
            retrieval_result[
                "retrieval_latency"
            ]
        )

        cda_error = (
            retrieval_result[
                "cda_error"
            ]
        )

        retrieval_error = (
            retrieval_result[
                "retrieval_error"
            ]
        )

        demand = retrieval_result[
            "demand"
        ]

        # Persist retrieved evidence before generation.
        self.write_json(
            os.path.join(
                artifact_dir,
                "retrieval_context.json",
            ),
            context_data,
        )

        if demand is not None:
            self.write_json(
                os.path.join(
                    artifact_dir,
                    "cda_demand.json",
                ),
                demand,
            )

        # ----------------------------------------------------
        # EXACT FINAL PROMPT
        # ----------------------------------------------------

        prompt = planner.build_prompt(
            user_query=query,
            query_id=query_id,
            mode=config[
                "type"
            ],
            context_data=context_data,
            use_ood_rule=config[
                "use_ood"
            ],
            use_template=config[
                "use_template"
            ],
        )

        prompt_sha256 = (
            self.sha256_text(
                prompt
            )
        )

        self.write_text(
            os.path.join(
                artifact_dir,
                "prompt.txt",
            ),
            prompt,
        )

        # ----------------------------------------------------
        # GENERATION / CACHE
        # ----------------------------------------------------

        generation_start = (
            time.perf_counter()
        )

        cache_hit = False
        generation_error = None
        raw_response = ""

        if (
            config[
                "use_cache"
            ]
            and prompt_sha256
            in self.response_cache
        ):
            raw_response = (
                self.response_cache[
                    prompt_sha256
                ]
            )

            cache_hit = True

        else:
            try:
                generation = (
                    planner.generate_with_metadata(
                        mode=config[
                            "type"
                        ],
                        user_query=query,
                        query_id=query_id,
                        context_data=context_data,
                        use_ood_rule=config[
                            "use_ood"
                        ],
                        use_template=config[
                            "use_template"
                        ],
                    )
                )

                raw_response = str(
                    generation.get(
                        "response",
                        "",
                    )
                )

                generated_prompt = str(
                    generation.get(
                        "prompt",
                        "",
                    )
                )

                generated_prompt_sha256 = str(
                    generation.get(
                        "prompt_sha256",
                        "",
                    )
                )

                # Strong reproducibility check:
                # the prompt generated for logging and the prompt used
                # for actual inference must be identical.
                if (
                    generated_prompt
                    != prompt
                ):
                    raise RuntimeError(
                        (
                            "Planner prompt mismatch: "
                            "build_prompt() != "
                            "generate_with_metadata()['prompt']"
                        )
                    )

                if (
                    generated_prompt_sha256
                    != prompt_sha256
                ):
                    raise RuntimeError(
                        (
                            "Planner prompt SHA256 mismatch."
                        )
                    )

                if config[
                    "use_cache"
                ]:
                    self.response_cache[
                        prompt_sha256
                    ] = raw_response

            except Exception as exc:
                generation_error = str(
                    exc
                )

                logging.error(
                    (
                        "Generation error | "
                        "model=%s | "
                        "architecture=%s | "
                        "query=%s | "
                        "error=%s"
                    ),
                    model_name,
                    mode_name,
                    query_id,
                    generation_error,
                )

                # CRITICAL:
                # Technical generation failure is NOT ABSTAIN.
                raw_response = ""

        generation_latency = round(
            time.perf_counter()
            - generation_start,
            4,
        )

        self.write_text(
            os.path.join(
                artifact_dir,
                "response.txt",
            ),
            raw_response,
        )

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        if generation_error:
            decision = "INVALID"
            decision_valid = False
            abstain_reason = None

        else:
            (
                decision,
                decision_valid,
                abstain_reason,
            ) = self.extract_decision(
                raw_response
            )

        # ----------------------------------------------------
        # CODE
        # ----------------------------------------------------

        code_extracted = (
            self.extract_python_code(
                raw_response
            )
        )

        # For ABSTAIN, code is intentionally not evaluated/executed.
        if (
            decision == "ANSWER"
            and decision_valid
        ):
            syntax_valid = (
                self.check_syntax(
                    code_extracted
                )
            )

        else:
            syntax_valid = False

        self.write_text(
            os.path.join(
                artifact_dir,
                "code.py",
            ),
            code_extracted,
        )

        # ----------------------------------------------------
        # FAILURE TYPE BEFORE EXECUTION
        # ----------------------------------------------------

        failure_type = (
            FAILURE_NONE
        )

        if generation_error:
            failure_type = (
                FAILURE_GENERATION
            )

        elif not decision_valid:
            failure_type = (
                FAILURE_INVALID_DECISION
            )

        elif (
            decision == "ANSWER"
            and not syntax_valid
        ):
            failure_type = (
                FAILURE_SYNTAX
            )

        # Non-terminal CDA/retrieval problems remain separately
        # recorded and do not get relabelled as abstention.
        pipeline_warnings: List[str] = []

        if cda_error:
            pipeline_warnings.append(
                FAILURE_CDA
            )

        if retrieval_error:
            pipeline_warnings.append(
                FAILURE_RETRIEVAL
            )

        # ----------------------------------------------------
        # EXECUTION
        # ----------------------------------------------------

        execution_payload = {
            "success": False,
            "status": (
                EXEC_NOT_REQUESTED
            ),
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "has_html": False,
            "timeout": False,
            "latency": 0.0,
        }

        if generation_error:
            execution_payload[
                "status"
            ] = EXEC_SKIPPED_GENERATION_ERROR

        elif not decision_valid:
            execution_payload[
                "status"
            ] = EXEC_SKIPPED_INVALID

        elif decision == "ABSTAIN":
            execution_payload[
                "status"
            ] = EXEC_SKIPPED_ABSTAIN

        elif not syntax_valid:
            execution_payload[
                "status"
            ] = EXEC_SKIPPED_SYNTAX

        else:
            execution_payload = (
                self.execute_code(
                    code_str=code_extracted,
                    output_html_name=(
                        f"{query_id}.html"
                    ),
                    use_sandbox=config[
                        "use_sandbox"
                    ],
                    artifact_dir=artifact_dir,
                )
            )

            if (
                execution_payload[
                    "status"
                ]
                == EXEC_TIMEOUT
            ):
                failure_type = (
                    FAILURE_TIMEOUT
                )

            elif (
                execution_payload[
                    "status"
                ]
                == EXEC_ERROR
            ):
                failure_type = (
                    FAILURE_EXECUTION
                )

        execution_latency = float(
            execution_payload[
                "latency"
            ]
        )

        # Persist diagnostics.
        self.write_text(
            os.path.join(
                artifact_dir,
                "stdout.txt",
            ),
            execution_payload[
                "stdout"
            ],
        )

        self.write_text(
            os.path.join(
                artifact_dir,
                "stderr.txt",
            ),
            execution_payload[
                "stderr"
            ],
        )

        # ----------------------------------------------------
        # RETRIEVAL METRICS
        # ----------------------------------------------------

        retrieval_metrics = None

        if config[
            "type"
        ] in {
            "vector_rag",
            "hydrographrag",
        }:
            retrieval_metrics = (
                self.calculate_retrieval_metrics(
                    retrieved_entities_list=(
                        retrieved_entities
                    ),
                    expected_entities=(
                        expected_entities
                    ),
                    triples_count=(
                        triples_count
                    ),
                )
            )

        # ----------------------------------------------------
        # TOTAL END-TO-END LATENCY
        # ----------------------------------------------------

        total_latency = round(
            time.perf_counter()
            - architecture_start,
            4,
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        prompt_metadata = {
            "prompt_sha256": (
                prompt_sha256
            ),
            "system_prompt_version": (
                getattr(
                    planner,
                    "SYSTEM_PROMPT_VERSION",
                    None,
                )
            ),
            "template_version": (
                getattr(
                    planner,
                    "TEMPLATE_VERSION",
                    None,
                )
                if config[
                    "use_template"
                ]
                else "disabled"
            ),
            "abstention_policy_version": (
                getattr(
                    planner,
                    "ABSTENTION_POLICY_VERSION",
                    None,
                )
                if config[
                    "use_ood"
                ]
                else "disabled"
            ),
            "model": model_name,
            "num_ctx": (
                GENERATION_CONFIG[
                    "context_size"
                ]
            ),
            "temperature": (
                GENERATION_CONFIG[
                    "temperature"
                ]
            ),
            "top_p": (
                GENERATION_CONFIG[
                    "top_p"
                ]
            ),
            "seed": (
                GENERATION_CONFIG[
                    "seed"
                ]
            ),
        }

        architecture_result: Dict[
            str,
            Any,
        ] = {
            # Decision
            "decision": decision,
            "decision_valid": (
                decision_valid
            ),
            "abstain_reason": (
                abstain_reason
            ),

            # Failure separation
            "failure_type": (
                failure_type
            ),
            "pipeline_warnings": (
                pipeline_warnings
            ),
            "generation_error": (
                generation_error
            ),
            "cda_error": (
                cda_error
            ),
            "retrieval_error": (
                retrieval_error
            ),

            # Reproducibility
            "prompt_sha256": (
                prompt_sha256
            ),
            # Backward-compatible alias.
            "prompt_hash": (
                prompt_sha256
            ),
            "prompt_metadata": (
                prompt_metadata
            ),
            "cache_hit": (
                cache_hit
            ),
            "cache_implementation": (
                CACHE_IMPLEMENTATION
                if config[
                    "use_cache"
                ]
                else "disabled"
            ),

            # CDA
            "cda_demand": (
                demand
            ),

            # Latency
            "cda_latency": (
                cda_latency
            ),
            "retrieval_latency": (
                retrieval_latency
            ),
            "generation_latency": (
                generation_latency
            ),
            "execution_latency": (
                execution_latency
            ),
            "total_latency": (
                total_latency
            ),

            # Code quality / execution
            "syntax": (
                syntax_valid
            ),
            "exec": bool(
                execution_payload[
                    "success"
                ]
            ),
            "has_map": bool(
                execution_payload[
                    "has_html"
                ]
            ),
            "execution_status": (
                execution_payload[
                    "status"
                ]
            ),
            "returncode": (
                execution_payload[
                    "returncode"
                ]
            ),
            "execution_timeout": bool(
                execution_payload[
                    "timeout"
                ]
            ),
            "stdout": (
                execution_payload[
                    "stdout"
                ]
            ),
            "stderr": (
                execution_payload[
                    "stderr"
                ]
            ),

            # Raw model output
            "raw_response": (
                raw_response
            ),
            "code_extracted": (
                code_extracted
            ),

            # Retrieval evidence
            "retrieval_context": (
                context_data
            ),
            "retrieved_entities": (
                retrieved_entities
            ),
            "retrieved_triples": (
                triples_count
            ),

            # Artifact directory relative to evaluation/
            "artifact_dir": (
                os.path.relpath(
                    artifact_dir,
                    EVAL_DIR,
                )
            ),
        }

        if retrieval_metrics is not None:
            architecture_result[
                "retrieval"
            ] = retrieval_metrics

        # Persist one compact metadata file per architecture/query.
        self.write_json(
            os.path.join(
                artifact_dir,
                "metadata.json",
            ),
            {
                "run_id": (
                    self.run_id
                ),
                "model": (
                    model_name
                ),
                "architecture": (
                    mode_name
                ),
                "query_id": (
                    query_id
                ),
                "category": (
                    category
                ),
                "config": (
                    config
                ),
                "result": (
                    architecture_result
                ),
            },
        )

        return (
            architecture_result
        )

    # ========================================================
    # EXPERIMENT MANIFEST
    # ========================================================

    def write_experiment_manifest(
        self,
        dataset: List[
            Dict[str, Any]
        ],
    ) -> None:
        with open(
            GROUND_TRUTH_PATH,
            "rb",
        ) as f:
            benchmark_sha256 = (
                hashlib.sha256(
                    f.read()
                ).hexdigest()
            )

        manifest = {
            "run_id": self.run_id,
            "created_at": (
                datetime.now().isoformat(
                    timespec="seconds"
                )
            ),
            "ground_truth_path": (
                GROUND_TRUTH_PATH
            ),
            "benchmark_sha256": (
                benchmark_sha256
            ),
            "dataset_size": len(
                dataset
            ),
            "generator_models": (
                GENERATOR_MODELS
            ),
            "generation_config": (
                GENERATION_CONFIG
            ),
            "execution_timeout_seconds": (
                EXECUTION_TIMEOUT_SECONDS
            ),
            "vector_top_k": (
                VECTOR_TOP_K
            ),
            "cache_implementation": (
                CACHE_IMPLEMENTATION
            ),
            "architectures": (
                ABLATION_MODES
            ),
            "python_executable": (
                sys.executable
            ),
        }

        self.write_json(
            EXPERIMENT_MANIFEST_PATH,
            manifest,
        )

    # ========================================================
    # CHECKPOINT
    # ========================================================

    @staticmethod
    def save_checkpoint(
        all_results: List[
            Dict[str, Any]
        ],
    ) -> None:
        with open(
            GENERATION_OUTPUT_PATH,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                all_results,
                f,
                ensure_ascii=False,
                indent=4,
                default=str,
            )

    # ========================================================
    # MAIN RUN
    # ========================================================

    def run(
        self,
        clean_run: bool = True,
    ) -> None:

        # ----------------------------------------------------
        # CLEAN RUN
        # ----------------------------------------------------

        if clean_run:
            if os.path.exists(
                GENERATION_OUTPUT_PATH
            ):
                logging.info(
                    (
                        "🧹 Clean run: removing old "
                        "generation_results.json"
                    )
                )

                os.remove(
                    GENERATION_OUTPUT_PATH
                )

            if os.path.exists(
                EXPERIMENT_MANIFEST_PATH
            ):
                os.remove(
                    EXPERIMENT_MANIFEST_PATH
                )

            if os.path.isdir(
                RESULTS_DIR
            ):
                logging.info(
                    (
                        "🧹 Clean run: removing old "
                        "results directory"
                    )
                )

                shutil.rmtree(
                    RESULTS_DIR
                )

        os.makedirs(
            RESULTS_DIR,
            exist_ok=True,
        )

        # ----------------------------------------------------
        # GROUND TRUTH
        # ----------------------------------------------------

        if not os.path.isfile(
            GROUND_TRUTH_PATH
        ):
            raise FileNotFoundError(
                (
                    "Ground Truth not found: "
                    f"{GROUND_TRUTH_PATH}"
                )
            )

        with open(
            GROUND_TRUTH_PATH,
            "r",
            encoding="utf-8",
        ) as f:
            dataset = json.load(
                f
            )

        if not isinstance(
            dataset,
            list,
        ):
            raise ValueError(
                (
                    "ground_truth.json must "
                    "contain a JSON list."
                )
            )

        self.write_experiment_manifest(
            dataset
        )

        # Reset cache for a genuinely cold run.
        self.response_cache.clear()

        all_results: List[
            Dict[str, Any]
        ] = []

        # ====================================================
        # MODELS
        # ====================================================

        for model_name in (
            GENERATOR_MODELS
        ):
            logging.info(
                (
                    "\n🚀 START MODEL: "
                    f"{model_name}"
                )
            )

            # ------------------------------------------------
            # COMPONENTS
            # ------------------------------------------------

            identifier = DemandIdentifier(
                model_name=model_name
            )

            retriever = GraphRetriever(
                self.db,
                self.embedder,
                model_name=model_name,
            )

            planner = SolutionPlanner(
                model_name=model_name,
                num_ctx=(
                    GENERATION_CONFIG[
                        "context_size"
                    ]
                ),
                temperature=(
                    GENERATION_CONFIG[
                        "temperature"
                    ]
                ),
                top_p=(
                    GENERATION_CONFIG[
                        "top_p"
                    ]
                ),
                seed=(
                    GENERATION_CONFIG[
                        "seed"
                    ]
                ),
            )

            model_results: List[
                Dict[str, Any]
            ] = []

            # =================================================
            # DATASET
            # =================================================

            for item in tqdm(
                dataset,
                desc=(
                    f"Testing {model_name}"
                ),
            ):
                if not isinstance(
                    item,
                    dict,
                ):
                    raise ValueError(
                        (
                            "Every ground-truth "
                            "item must be a dict."
                        )
                    )

                query = str(
                    item.get(
                        "query",
                        "",
                    )
                ).strip()

                query_id = str(
                    item.get(
                        "id",
                        "",
                    )
                ).strip()

                category = str(
                    item.get(
                        "category",
                        "",
                    )
                ).strip().lower()

                expected_entities = (
                    item.get(
                        "expected_entities",
                        [],
                    )
                )

                if not query:
                    raise ValueError(
                        (
                            "Empty query for "
                            f"ID={query_id}"
                        )
                    )

                if not query_id:
                    raise ValueError(
                        "Missing query ID."
                    )

                query_result: Dict[
                    str,
                    Any,
                ] = {
                    "query_id": (
                        query_id
                    ),
                    "query": query,
                    "category": category,
                }

                # =============================================
                # ARCHITECTURES
                # =============================================

                for (
                    mode_name,
                    config,
                ) in (
                    ABLATION_MODES.items()
                ):
                    try:
                        architecture_result = (
                            self.run_architecture(
                                model_name=(
                                    model_name
                                ),
                                query=query,
                                query_id=(
                                    query_id
                                ),
                                category=(
                                    category
                                ),
                                expected_entities=(
                                    expected_entities
                                ),
                                mode_name=(
                                    mode_name
                                ),
                                config=(
                                    config
                                ),
                                identifier=(
                                    identifier
                                ),
                                retriever=(
                                    retriever
                                ),
                                planner=(
                                    planner
                                ),
                            )
                        )

                    except Exception as exc:
                        # Catastrophic architecture-level failure.
                        # It is explicitly INVALID, never ABSTAIN.
                        error = str(
                            exc
                        )

                        logging.exception(
                            (
                                "Architecture failure | "
                                "model=%s | "
                                "architecture=%s | "
                                "query=%s"
                            ),
                            model_name,
                            mode_name,
                            query_id,
                        )

                        architecture_result = {
                            "decision": (
                                "INVALID"
                            ),
                            "decision_valid": False,
                            "abstain_reason": None,
                            "failure_type": (
                                FAILURE_GENERATION
                            ),
                            "pipeline_warnings": [],
                            "generation_error": (
                                error
                            ),
                            "cda_error": None,
                            "retrieval_error": None,
                            "syntax": False,
                            "exec": False,
                            "has_map": False,
                            "execution_status": (
                                EXEC_SKIPPED_GENERATION_ERROR
                            ),
                            "returncode": None,
                            "execution_timeout": False,
                            "stdout": "",
                            "stderr": error,
                            "raw_response": "",
                            "code_extracted": "",
                            "retrieval_context": [],
                            "retrieved_entities": [],
                            "retrieved_triples": 0,
                            "cda_latency": 0.0,
                            "retrieval_latency": 0.0,
                            "generation_latency": 0.0,
                            "execution_latency": 0.0,
                            "total_latency": 0.0,
                            "cache_hit": False,
                            "prompt_sha256": None,
                            "prompt_hash": None,
                            "prompt_metadata": {},
                        }

                    query_result[
                        mode_name
                    ] = architecture_result

                model_results.append(
                    query_result
                )

            # =================================================
            # MODEL RESULT
            # =================================================

            model_result = {
                "model": model_name,
                "role": "generator",
                "run_id": self.run_id,
                "quantization": "Q4_K_M",
                "generation_config": (
                    GENERATION_CONFIG
                ),
                "ablation_modes": (
                    ABLATION_MODES
                ),
                "metrics": (
                    model_results
                ),
            }

            all_results.append(
                model_result
            )

            # Checkpoint after every model.
            self.save_checkpoint(
                all_results
            )

            logging.info(
                (
                    "💾 Results saved for "
                    f"{model_name}"
                )
            )

        # ========================================================
        # FINISH
        # ========================================================

        logging.info(
            (
                "🎉 Generation / Ablation "
                "pipeline completed."
            )
        )

        logging.info(
            (
                "📄 Results: "
                f"{GENERATION_OUTPUT_PATH}"
            )
        )

        logging.info(
            (
                "📁 Raw artifacts: "
                f"{RESULTS_DIR}"
            )
        )

        logging.info(
            (
                "🧾 Experiment manifest: "
                f"{EXPERIMENT_MANIFEST_PATH}"
            )
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    pipeline = (
        GenerationPipeline()
    )

    pipeline.run(
        clean_run=True
    )