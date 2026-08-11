import ast
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time

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
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ============================================================
# PATHS
# ============================================================

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))

GROUND_TRUTH_PATH = os.path.join(
    EVAL_DIR,
    "ground_truth.json"
)

GENERATION_OUTPUT_PATH = os.path.join(
    EVAL_DIR,
    "generation_results.json"
)

RESULTS_DIR = os.path.join(
    EVAL_DIR,
    "results"
)


# ============================================================
# REPRODUCIBILITY CONFIGURATION
# ============================================================

GENERATION_CONFIG = {
    "temperature": 0.0,
    "top_p": 1.0,
    "seed": 42,
    "context_size": 32768
}


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
    "gemma4:31b"
]


# ============================================================
# ABLATION STUDY
# ============================================================

ABLATION_MODES = {

    # ----------------------------
    # Baseline
    # ----------------------------

    "Baseline": {
        "type": "baseline",
        "use_cda": False,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    # ----------------------------
    # Vector RAG
    # ----------------------------

    "VectorRAG": {
        "type": "vector_rag",
        "use_cda": False,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    # ----------------------------
    # Full HydroGraphRAG
    # ----------------------------

    "HydroGraphRAG": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: CDA
    # ----------------------------

    "HydroGraphRAG_no_CDA": {
        "type": "hydrographrag",
        "use_cda": False,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: WKT
    # ----------------------------

    "HydroGraphRAG_no_WKT": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": False,
        "use_ood": True,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: Template
    # ----------------------------

    "HydroGraphRAG_no_Template": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": False,
        "use_cache": True,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: OOD
    # ----------------------------

    "HydroGraphRAG_no_OOD": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": False,
        "use_template": True,
        "use_cache": True,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: Cache
    # ----------------------------

    "HydroGraphRAG_no_Cache": {
        "type": "hydrographrag",
        "use_cda": True,
        "use_wkt": True,
        "use_ood": True,
        "use_template": True,
        "use_cache": False,
        "use_sandbox": True,
    },

    # ----------------------------
    # Ablation: Sandbox
    # ----------------------------

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
# PIPELINE
# ============================================================

class GenerationPipeline:

    def __init__(self):

        logging.info(
            "⏳ Инициализация среды тестирования..."
        )

        self.db = HydroDatabase()
        self.embedder = EmbeddingsManager()

        # Реальный in-memory semantic cache.
        self.semantic_cache = {}


    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize_entity(self, text):
        """
        Нормализация entity для retrieval metrics.

        Важно:
        - регистр игнорируется;
        - лишние пробелы удаляются;
        - цифры НЕ удаляются.

        Поэтому:
            Station 17
            station 17

        считаются одной entity.
        """

        return re.sub(
            r"\s+",
            " ",
            str(text).strip().lower()
        )


    # ========================================================
    # CODE EXTRACTION
    # ========================================================

    def extract_python_code(self, text):
        """
        Извлекает Python-код из ответа LLM.

        Поддерживает:
            ```python
            ...
            ```

        и обычный:

            ```
            ...
            ```

        Если markdown-блока нет, возвращается весь ответ.
        """

        if not text:
            return ""

        text = str(text)

        python_match = re.search(
            r"```python\s*\n(.*?)```",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if python_match:
            return python_match.group(1).strip()

        generic_match = re.search(
            r"```\s*\n?(.*?)```",
            text,
            re.DOTALL
        )

        if generic_match:
            return generic_match.group(1).strip()

        return text.strip()


    # ========================================================
    # DECISION EXTRACTION
    # ========================================================

    def extract_decision(self, text):
        """
        Извлекает decision и abstain_reason.

        Валидные решения:
            ANSWER
            ABSTAIN

        Если decision отсутствует:
            INVALID
        """

        if not text:
            return "INVALID", False, None

        decision_match = re.search(
            r"decision\s*:\s*(ANSWER|ABSTAIN)",
            text,
            re.IGNORECASE
        )

        if decision_match:

            decision = decision_match.group(1).upper()
            decision_valid = True

        else:

            decision = "INVALID"
            decision_valid = False

        reason_match = re.search(
            r"abstain_reason\s*:\s*(.*)",
            text,
            re.IGNORECASE
        )

        reason = (
            reason_match.group(1).strip()
            if reason_match
            else None
        )

        return decision, decision_valid, reason


    # ========================================================
    # SYNTAX CHECK
    # ========================================================

    def check_syntax(self, code_str):
        """
        Проверяет синтаксис без выполнения кода.
        """

        try:

            clean_code = self.extract_python_code(code_str)

            if not clean_code:
                return False

            ast.parse(clean_code)

            return True

        except Exception:

            return False


    # ========================================================
    # CODE EXECUTION
    # ========================================================

    def execute_code(
        self,
        code_str,
        output_html_name,
        use_sandbox
    ):
        """
        Выполняет сгенерированный код.

        use_sandbox=True:
            - отдельная временная директория;
            - timeout 15 секунд;
            - данные копируются в sandbox.

        use_sandbox=False:
            - честная ablation;
            - код запускается непосредственно в EVAL_DIR;
            - timeout 120 секунд.

        Возвращает:

            execution_success,
            error_message,
            has_html
        """

        clean_code = self.extract_python_code(code_str)

        if not clean_code or len(clean_code.strip()) < 10:

            return (
                False,
                "No valid code found",
                False
            )


        # ====================================================
        # SANDBOX MODE
        # ====================================================

        if use_sandbox:

            with tempfile.TemporaryDirectory(
                prefix="hydro_eval_"
            ) as local_sandbox:

                tmp_py = os.path.join(
                    local_sandbox,
                    "script.py"
                )

                with open(
                    tmp_py,
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(clean_code)


                # Копируем геоданные в sandbox.

                data_src = os.path.join(
                    EVAL_DIR,
                    "data"
                )

                data_dest = os.path.join(
                    local_sandbox,
                    "data"
                )

                if os.path.exists(data_src):

                    shutil.copytree(
                        data_src,
                        data_dest
                    )


                try:

                    result = subprocess.run(
                        [
                            "python",
                            "script.py"
                        ],
                        cwd=local_sandbox,
                        capture_output=True,
                        text=True,
                        timeout=15
                    )

                    html_path = os.path.join(
                        local_sandbox,
                        output_html_name
                    )

                    has_html = os.path.exists(
                        html_path
                    )

                    if result.returncode == 0:

                        return (
                            True,
                            "Success",
                            has_html
                        )

                    return (
                        False,
                        result.stderr,
                        has_html
                    )

                except subprocess.TimeoutExpired:

                    return (
                        False,
                        "Execution timeout (15 seconds)",
                        False
                    )

                except Exception as e:

                    return (
                        False,
                        str(e),
                        False
                    )


        # ====================================================
        # NO-SANDBOX MODE
        # ====================================================

        else:

            # Честная абляция:
            # запуск непосредственно на host environment.

            tmp_py = os.path.join(
                EVAL_DIR,
                f"unsafe_script_{os.getpid()}_{int(time.time() * 1000)}.py"
            )

            html_path = os.path.join(
                EVAL_DIR,
                output_html_name
            )

            try:

                with open(
                    tmp_py,
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(clean_code)


                result = subprocess.run(
                    [
                        "python",
                        os.path.basename(tmp_py)
                    ],
                    cwd=EVAL_DIR,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                has_html = os.path.exists(
                    html_path
                )

                if result.returncode == 0:

                    return (
                        True,
                        "Success",
                        has_html
                    )

                return (
                    False,
                    result.stderr,
                    has_html
                )

            except subprocess.TimeoutExpired:

                return (
                    False,
                    "Execution timeout (120 seconds)",
                    False
                )

            except Exception as e:

                return (
                    False,
                    str(e),
                    False
                )

            finally:

                # Всегда удаляем временный Python-файл.

                if os.path.exists(tmp_py):

                    try:
                        os.remove(tmp_py)

                    except OSError:
                        pass

                # HTML тоже удаляем после no-sandbox execution.

                if os.path.exists(html_path):

                    try:
                        os.remove(html_path)

                    except OSError:
                        pass


    # ========================================================
    # VECTOR RETRIEVAL
    # ========================================================

    def get_vector_context(
        self,
        query,
        retriever,
        k=5
    ):
        """
        Настоящий vector retrieval.

        Возвращает:

            context_string,
            entity_list
        """

        try:

            candidates = retriever._get_all_entities()

            scored = self.embedder.find_top_matches(
                query,
                candidates,
                top_k=k
            )

            entities = []
            context_lines = []

            for item in scored:

                entity = item[0]

                entity_name = entity.get(
                    "name",
                    ""
                )

                entities.append(
                    entity_name
                )

                context_lines.append(
                    f"Entity: {entity_name} "
                    f"(Type: {entity.get('category', 'Unknown')})"
                )

            return (
                "\n".join(context_lines),
                entities
            )

        except Exception as e:

            logging.warning(
                f"VectorRAG Context Error: {e}"
            )

            return (
                "No external context found.",
                []
            )


    # ========================================================
    # GRAPH ENTITY EXTRACTION
    # ========================================================

    def extract_entities_from_triples(
        self,
        triples
    ):
        """
        Извлекает entities из graph triples.

        Цифры НЕ фильтруются.

        Поэтому:
            Station 17
            River-42

        остаются валидными entities.
        """

        entities = set()

        technical_words = {
            "region",
            "class",
            "value",
            "unit",
            "geometry",
            "haswkt",
            "date"
        }

        if not isinstance(triples, list):

            return []


        for triple in triples:

            if not isinstance(triple, dict):
                continue

            nodes = [
                triple.get("from", ""),
                triple.get("to", "")
            ]

            for node in nodes:

                node_clean = self.normalize_entity(
                    node
                )

                if len(node_clean) <= 2:
                    continue

                if any(
                    word in node_clean
                    for word in technical_words
                ):
                    continue

                entities.add(node_clean)

        return list(entities)


    # ========================================================
    # RETRIEVAL METRICS
    # ========================================================

    def calculate_retrieval_metrics(
        self,
        retrieved_entities_list,
        expected_entities,
        triples_count=0
    ):
        """
        Entity-level Precision / Recall / F1.

        Особый случай:

        expected = []
        retrieved = []

        означает корректное отсутствие entities:

            precision = 1
            recall = 1
            F1 = 1

        Если expected пустой, но retriever вернул entities:

            precision = 0
            recall = 0
            F1 = 0
        """

        expected_entities = (
            expected_entities
            if expected_entities
            else []
        )

        retrieved_entities_list = (
            retrieved_entities_list
            if retrieved_entities_list
            else []
        )


        # -----------------------------------------------
        # True empty retrieval
        # -----------------------------------------------

        if (
            not expected_entities
            and not retrieved_entities_list
        ):

            return {
                "precision": 1.0,
                "recall": 1.0,
                "f1": 1.0,
                "retrieved_entities": 0,
                "targets_found": 0,
                "retrieved_triples": triples_count
            }


        # -----------------------------------------------
        # Hallucinated retrieval
        # -----------------------------------------------

        if (
            not expected_entities
            and retrieved_entities_list
        ):

            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "retrieved_entities": len(
                    retrieved_entities_list
                ),
                "targets_found": 0,
                "retrieved_triples": triples_count
            }


        # -----------------------------------------------
        # Normal case
        # -----------------------------------------------

        truth_nodes = {
            self.normalize_entity(entity)
            for entity in expected_entities
        }

        retrieved_nodes = {
            self.normalize_entity(entity)
            for entity in retrieved_entities_list
        }

        matched = truth_nodes & retrieved_nodes

        true_positive = len(matched)

        retrieved_count = len(
            retrieved_nodes
        )

        expected_count = len(
            truth_nodes
        )

        precision = (
            true_positive / retrieved_count
            if retrieved_count > 0
            else 0.0
        )

        recall = (
            true_positive / expected_count
            if expected_count > 0
            else 0.0
        )

        f1 = (
            2 * precision * recall /
            (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "targets_found": true_positive,
            "retrieved_entities": retrieved_count,
            "retrieved_triples": triples_count
        }


    # ========================================================
    # CACHE HASH
    # ========================================================

    def make_cache_hash(
        self,
        model_name,
        query,
        mode_name,
        config,
        context_data
    ):
        """
        Создаёт детерминированный hash полного prompt-relevant
        состояния.

        В hash входят:

        - model;
        - query;
        - architecture;
        - CDA;
        - WKT;
        - OOD;
        - template;
        - context.

        use_cache намеренно НЕ входит:
        наличие cache не должно менять сам prompt.
        """

        cache_payload = {
            "model": model_name,
            "query": query,
            "architecture": mode_name,
            "mode": config["type"],
            "use_cda": config["use_cda"],
            "use_wkt": config["use_wkt"],
            "use_ood": config["use_ood"],
            "use_template": config["use_template"],
            "context": context_data,
        }

        canonical_payload = json.dumps(
            cache_payload,
            ensure_ascii=False,
            sort_keys=True,
            default=str
        )

        return hashlib.sha256(
            canonical_payload.encode("utf-8")
        ).hexdigest()


    # ========================================================
    # MAIN RUN
    # ========================================================

    def run(self, clean_run=True):

        # ----------------------------------------------------
        # Clean run
        # ----------------------------------------------------

        if (
            clean_run
            and os.path.exists(GENERATION_OUTPUT_PATH)
        ):

            logging.info(
                "🧹 Clean Run: удаляем старый generation_results.json"
            )

            os.remove(
                GENERATION_OUTPUT_PATH
            )


        # ----------------------------------------------------
        # Ground Truth
        # ----------------------------------------------------

        if not os.path.exists(
            GROUND_TRUTH_PATH
        ):

            raise FileNotFoundError(
                f"Ground Truth не найден: "
                f"{GROUND_TRUTH_PATH}"
            )


        with open(
            GROUND_TRUTH_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            dataset = json.load(f)


        # ----------------------------------------------------
        # Results directory
        # ----------------------------------------------------

        os.makedirs(
            RESULTS_DIR,
            exist_ok=True
        )


        all_results = []


        # ====================================================
        # MODELS
        # ====================================================

        for model_name in GENERATOR_MODELS:

            logging.info(
                f"\n🚀 СТАРТ ТЕСТА МОДЕЛИ: {model_name}"
            )


            safe_model_name = model_name.replace(
                ":",
                "_"
            )

            model_dir = os.path.join(
                RESULTS_DIR,
                safe_model_name
            )

            os.makedirs(
                model_dir,
                exist_ok=True
            )


            # Создаём директории всех архитектур.

            for mode_name in ABLATION_MODES:

                os.makedirs(
                    os.path.join(
                        model_dir,
                        mode_name
                    ),
                    exist_ok=True
                )


            # ------------------------------------------------
            # Components
            # ------------------------------------------------

            identifier = DemandIdentifier(
                model_name=model_name
            )

            retriever = GraphRetriever(
                self.db,
                self.embedder,
                model_name=model_name
            )

            planner = SolutionPlanner(
                model_name=model_name
            )


            model_results = []


            # =================================================
            # DATASET
            # =================================================

            for item in tqdm(
                dataset,
                desc=f"Testing {model_name}"
            ):

                query = item["query"]

                query_id = str(
                    item.get("id")
                )

                category = item.get(
                    "category"
                )

                expected_entities = item.get(
                    "expected_entities",
                    []
                )


                # ------------------------------------------------
                # CDA
                # ------------------------------------------------

                cda_start = time.time()

                try:

                    cda_demand = identifier.analyze_query(
                        query
                    )

                except Exception as e:

                    logging.warning(
                        f"CDA error for query {query_id}: {e}"
                    )

                    cda_demand = {
                        "category": "explicit",
                        "extracted_inputs": [query]
                    }

                cda_latency = round(
                    time.time() - cda_start,
                    4
                )


                # ------------------------------------------------
                # Vector retrieval
                # ------------------------------------------------

                vector_start = time.time()

                vec_context_str, vec_entities = (
                    self.get_vector_context(
                        query,
                        retriever
                    )
                )

                vector_latency = round(
                    time.time() - vector_start,
                    4
                )


                query_result = {
                    "query_id": query_id,
                    "category": category,
                    "cda_latency": cda_latency,
                    "vector_retrieval_latency": vector_latency
                }


                # =================================================
                # ARCHITECTURES
                # =================================================

                for mode_name, config in ABLATION_MODES.items():

                    retrieval_start = time.time()

                    retrieved_entities = []
                    triples_count = 0
                    context_data = []


                    # =============================================
                    # BASELINE
                    # =============================================

                    if config["type"] == "baseline":

                        context_data = []


                    # =============================================
                    # VECTOR RAG
                    # =============================================

                    elif config["type"] == "vector_rag":

                        context_data = vec_context_str

                        retrieved_entities = vec_entities


                    # =============================================
                    # HYDROGRAPH RAG
                    # =============================================

                    else:

                        if config["use_cda"]:

                            demand = cda_demand

                        else:

                            demand = {
                                "category": "explicit",
                                "extracted_inputs": [query]
                            }


                        try:

                            raw_triples = (
                                retriever.find_solution_subgraph(
                                    demand
                                )
                            )

                        except Exception as e:

                            logging.warning(
                                f"Graph retrieval error "
                                f"for {query_id} / {mode_name}: {e}"
                            )

                            raw_triples = []


                        if config["use_wkt"]:

                            context_data = raw_triples

                        else:

                            context_data = [
                                triple
                                for triple in raw_triples
                                if triple.get("rel") != "hasWKT"
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
                        time.time() - retrieval_start,
                        4
                    )


                    # =================================================
                    # CACHE
                    # =================================================

                    prompt_hash = self.make_cache_hash(
                        model_name=model_name,
                        query=query,
                        mode_name=mode_name,
                        config=config,
                        context_data=context_data
                    )


                    cache_hit = False


                    generation_start = time.time()


                    if (
                        config["use_cache"]
                        and prompt_hash in self.semantic_cache
                    ):

                        res_llm = self.semantic_cache[
                            prompt_hash
                        ]

                        cache_hit = True


                    else:

                        try:

                            res_llm = planner.generate(
                                mode=config["type"],
                                user_query=query,
                                query_id=query_id,
                                context_data=context_data,
                                use_ood_rule=config["use_ood"],
                                use_template=config["use_template"]
                            )

                        except Exception as e:

                            logging.error(
                                f"Generation error "
                                f"{model_name} / "
                                f"{mode_name} / "
                                f"{query_id}: {e}"
                            )

                            res_llm = (
                                f"decision: ABSTAIN\n"
                                f"abstain_reason: "
                                f"Generation exception: {e}"
                            )


                        if config["use_cache"]:

                            self.semantic_cache[
                                prompt_hash
                            ] = res_llm


                    generation_latency = round(
                        time.time() - generation_start,
                        4
                    )

                    total_latency = round(
                        retrieval_latency +
                        generation_latency,
                        4
                    )


                    # =================================================
                    # RESPONSE PROCESSING
                    # =================================================

                    code_extracted = (
                        self.extract_python_code(
                            res_llm
                        )
                    )

                    syntax_valid = (
                        self.check_syntax(
                            code_extracted
                        )
                    )

                    decision, decision_valid, abstain_reason = (
                        self.extract_decision(
                            res_llm
                        )
                    )


                    # =================================================
                    # SAVE PYTHON CODE
                    # =================================================

                    py_path = os.path.join(
                        model_dir,
                        mode_name,
                        f"{query_id}.py"
                    )

                    with open(
                        py_path,
                        "w",
                        encoding="utf-8"
                    ) as f:

                        f.write(
                            code_extracted
                        )


                    # =================================================
                    # EXECUTION
                    # =================================================

                    execution_success = False
                    execution_error = "Not Executed"
                    has_map = False


                    if syntax_valid:

                        (
                            execution_success,
                            execution_error,
                            has_map
                        ) = self.execute_code(
                            code_extracted,
                            f"{query_id}.html",
                            config["use_sandbox"]
                        )


                    # =================================================
                    # ARCHITECTURE RESULTS
                    # =================================================

                    architecture_result = {

                        # -----------------------------
                        # Decision
                        # -----------------------------

                        "decision": decision,
                        "decision_valid": decision_valid,
                        "abstain_reason": abstain_reason,

                        # -----------------------------
                        # Reproducibility
                        # -----------------------------

                        "prompt_hash": prompt_hash,
                        "cache_hit": cache_hit,

                        # -----------------------------
                        # Latency
                        # -----------------------------

                        "retrieval_latency": retrieval_latency,
                        "generation_latency": generation_latency,
                        "total_latency": total_latency,

                        # -----------------------------
                        # Code quality
                        # -----------------------------

                        "syntax": syntax_valid,
                        "exec": execution_success,
                        "has_map": has_map,

                        # -----------------------------
                        # Full model response
                        # IMPORTANT FOR JUDGE
                        # -----------------------------

                        "raw_response": res_llm,

                        # -----------------------------
                        # Extracted code
                        # -----------------------------

                        "code_extracted": code_extracted,

                        # -----------------------------
                        # Execution diagnostics
                        # -----------------------------

                        "execution_error": execution_error,

                        # -----------------------------
                        # Retrieval metadata
                        # -----------------------------

                        "retrieval_context": context_data,
                        "retrieved_entities": retrieved_entities,
                        "retrieved_triples": triples_count,
                    }


                    # =================================================
                    # RETRIEVAL METRICS
                    # =================================================

                    if config["type"] in (
                        "hydrographrag",
                        "vector_rag"
                    ):

                        architecture_result[
                            "retrieval"
                        ] = self.calculate_retrieval_metrics(
                            retrieved_entities,
                            expected_entities,
                            triples_count
                        )


                    # =================================================
                    # STORE RESULT
                    # =================================================

                    query_result[
                        mode_name
                    ] = architecture_result


                # ----------------------------------------------------
                # Store query
                # ----------------------------------------------------

                model_results.append(
                    query_result
                )


            # ========================================================
            # MODEL RESULT
            # ========================================================

            model_result = {

                "model": model_name,

                "role": "generator",

                "quantization": "Q4_K_M",

                "generation_config": GENERATION_CONFIG,

                "ablation_modes": ABLATION_MODES,

                "metrics": model_results
            }


            all_results.append(
                model_result
            )


            # ========================================================
            # CHECKPOINT
            # ========================================================

            with open(
                GENERATION_OUTPUT_PATH,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    all_results,
                    f,
                    ensure_ascii=False,
                    indent=4
                )


            logging.info(
                f"💾 Результаты {model_name} сохранены."
            )


        # ========================================================
        # FINISH
        # ========================================================

        logging.info(
            "🎉 Пайплайн Generation / Ablation Study завершён."
        )

        logging.info(
            f"📄 Результаты: {GENERATION_OUTPUT_PATH}"
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    pipeline = GenerationPipeline()

    pipeline.run(
        clean_run=True
    )
