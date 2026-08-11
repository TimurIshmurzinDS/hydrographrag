import json
import logging
import re
import os
import ast
import pandas as pd
from tqdm import tqdm
from langchain_ollama import ChatOllama

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ============================================================
# CONFIG
# ============================================================

JUDGE_MODEL = "qwen2.5:72b-instruct"

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_PATH = os.path.join(
    EVAL_DIR,
    "generation_results.json"
)

FINAL_OUTPUT_PATH = os.path.join(
    EVAL_DIR,
    "final_evaluation_results.json"
)

GROUND_TRUTH_PATH = os.path.join(
    EVAL_DIR,
    "ground_truth.json"
)

HALLUCINATION_DETAILS_PATH = os.path.join(
    EVAL_DIR,
    "hallucination_subtypes_detailed.csv"
)

HALLUCINATION_SUMMARY_PATH = os.path.join(
    EVAL_DIR,
    "hallucination_subtypes.csv"
)


# ============================================================
# EVALUATION PIPELINE
# ============================================================

class EvaluationPipeline:

    def __init__(self):

        logging.info(
            f"⚖️ Инициализация судьи {JUDGE_MODEL} "
            f"(temperature=0, seed=42)"
        )

        self.judge = ChatOllama(
            model=JUDGE_MODEL,
            temperature=0.0,
            top_p=1.0,
            num_ctx=8192,
            seed=42
        )

    # ========================================================
    # ROBUST JSON PARSER
    # ========================================================

    def _robust_json_parse(self, text):

        if not text:
            return None

        try:

            # Убираем reasoning/thinking блоки
            text = re.sub(
                r"<think>.*?</think>",
                "",
                text,
                flags=re.DOTALL | re.IGNORECASE
            ).strip()

            # Убираем markdown fences
            text = text.replace("```json", "")
            text = text.replace("```", "").strip()

            # Ищем JSON object
            match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            json_str = match.group(0) if match else text

            # Сначала обычный JSON
            try:
                return json.loads(json_str)

            except json.JSONDecodeError:

                # Fallback для Python-style dict
                try:
                    return ast.literal_eval(json_str)

                except Exception:
                    return None

        except Exception:
            return None

    # ========================================================
    # CONTEXT SERIALIZATION
    # ========================================================

    def _format_retrieved_context(self, mode_result):

        """
        В generation_results retrieval context напрямую не сохраняется
        как отдельное поле, поэтому здесь используем сохранённые данные,
        если они присутствуют.

        Поддерживаются:
        - retrieved_context
        - context_data
        - retrieval_context

        Если их нет — возвращаем честное сообщение.
        """

        context = (
            mode_result.get("retrieved_context")
            or mode_result.get("context_data")
            or mode_result.get("retrieval_context")
        )

        if context is None:
            return (
                "RETRIEVED CONTEXT WAS NOT STORED IN "
                "generation_results.json."
            )

        if isinstance(context, list):

            lines = []

            for i, item in enumerate(context, 1):

                if isinstance(item, dict):

                    source = item.get(
                        "from",
                        item.get("source", "")
                    )

                    relation = item.get(
                        "rel",
                        item.get("relation", "")
                    )

                    target = item.get(
                        "to",
                        item.get("target", "")
                    )

                    lines.append(
                        f"{i}. {source} -[{relation}]-> {target}"
                    )

                else:
                    lines.append(
                        f"{i}. {str(item)}"
                    )

            return "\n".join(lines)

        return str(context)

    # ========================================================
    # GROUND TRUTH FORMATTER
    # ========================================================

    def _format_ground_truth(self, gt_item):

        return f"""
Expected Entities:
{json.dumps(
    gt_item.get("expected_entities", []),
    ensure_ascii=False
)}

Expected Relations:
{json.dumps(
    gt_item.get("expected_relations", []),
    ensure_ascii=False
)}

Expected Triples:
{json.dumps(
    gt_item.get("expected_triples", []),
    ensure_ascii=False
)}

Expected WKT:
{json.dumps(
    gt_item.get("expected_wkt", []),
    ensure_ascii=False
)}

Expected Numeric Values:
{json.dumps(
    gt_item.get("expected_numeric_facts", []),
    ensure_ascii=False
)}

Expected Temporal Facts:
{json.dumps(
    gt_item.get("expected_temporal_facts", []),
    ensure_ascii=False
)}

Expected Categories:
{json.dumps(
    gt_item.get("expected_categories", []),
    ensure_ascii=False
)}

Expected Topology:
{json.dumps(
    gt_item.get("expected_topology", []),
    ensure_ascii=False
)}
""".strip()

    # ========================================================
    # JUDGE
    # ========================================================

    def evaluate(
        self,
        query,
        mode_name,
        mode_result,
        gt_item
    ):

        exec_status = mode_result.get(
            "exec",
            False
        )

        syntax_status = mode_result.get(
            "syntax",
            False
        )

        has_map = mode_result.get(
            "has_map",
            False
        )

        decision = mode_result.get(
            "decision",
            "INVALID"
        )

        decision_valid = mode_result.get(
            "decision_valid",
            False
        )

        raw_response = mode_result.get(
            "raw_response",
            ""
        )

        code_extracted = mode_result.get(
            "code_extracted",
            ""
        )

        retrieved_context = self._format_retrieved_context(
            mode_result
        )

        ground_truth = self._format_ground_truth(
            gt_item
        )

        execution_status = (
            "SUCCESS"
            if exec_status
            else "FAILED"
        )

        syntax_status_text = (
            "VALID"
            if syntax_status
            else "INVALID"
        )

        map_status = (
            "GENERATED"
            if has_map
            else "NOT GENERATED"
        )

        # ====================================================
        # STRICT JUDGE PROMPT
        # ====================================================

        prompt = f"""
You are a senior geospatial and hydrology researcher evaluating
an AI GeoGraphRAG framework.

Your task is to evaluate ONE generated answer against the
Ground Truth and the information actually available to the generator.

Do NOT reward plausible information that is not supported by
the provided Ground Truth or Retrieved Context.

============================================================
USER QUERY
============================================================

{query}

============================================================
GROUND TRUTH
============================================================

{ground_truth}

============================================================
RETRIEVED CONTEXT AVAILABLE TO THE GENERATOR
============================================================

{retrieved_context}

============================================================
MODEL EXECUTION METADATA
============================================================

Architecture:
{mode_name}

Decision:
{decision}

Decision valid:
{decision_valid}

Python syntax:
{syntax_status_text}

Execution:
{execution_status}

HTML map:
{map_status}

============================================================
EXTRACTED PYTHON CODE
============================================================

{code_extracted}

============================================================
RAW MODEL RESPONSE
============================================================

{raw_response}

============================================================
SCORING
============================================================

Score every dimension from 1 to 5.

5 = Fully correct / exactly supported
4 = Mostly correct; only minor issue
3 = Partially correct; meaningful omissions or inaccuracies
2 = Mostly incorrect
1 = Completely incorrect, fabricated, or unsupported

------------------------------------------------------------
1. semantic_score
------------------------------------------------------------

Evaluate whether the answer correctly understands and addresses
the user's actual hydrology/GIS request.

------------------------------------------------------------
2. structural_score
------------------------------------------------------------

Evaluate whether the response follows the required structure:

### Modeling Solution:
...
### Implementation Code:
...

Also consider whether the generated Python code is clearly separated
from the explanation.

A syntax error alone should not automatically make this score 1;
evaluate the response structure itself.

------------------------------------------------------------
3. faithfulness_score
------------------------------------------------------------

Evaluate factual faithfulness.

IMPORTANT:

A claim is supported if it is present in either:

1. Ground Truth
2. Retrieved Context

If the model introduces a factual claim that is not supported by
either source, treat it as unsupported/hallucinated.

Do NOT assume that a plausible real-world fact is correct merely
because it sounds reasonable.

------------------------------------------------------------
4. spatial_score
------------------------------------------------------------

Evaluate spatial information:

- WKT
- coordinates
- geometry
- map locations

Compare generated spatial information against Expected WKT.

If Expected WKT is empty:

- no invented spatial information = 5
- invented coordinates/WKT = 1

------------------------------------------------------------
5. numerical_score
------------------------------------------------------------

Evaluate:

- water level
- discharge
- measurements
- population
- areas
- other numerical facts

Compare against Ground Truth and Retrieved Context.

If a numerical fact is not supported, treat it as hallucinated.

If Expected Numeric Values is empty:

- no invented numerical facts = 5
- invented numerical facts = 1

------------------------------------------------------------
6. topological_score
------------------------------------------------------------

Evaluate graph relationships such as:

- upstream/downstream
- river connections
- located-in relationships
- region relationships
- station/river relationships

Do not infer correctness from general world knowledge.

Use only Ground Truth and Retrieved Context.

------------------------------------------------------------
7. categorical_score
------------------------------------------------------------

Evaluate:

- entity categories
- sensor/status classifications
- region names
- object types
- categorical attributes

Again, use Ground Truth and Retrieved Context.

============================================================
EMPTY GROUND TRUTH RULE
============================================================

For every specific Ground Truth array:

If the array is EMPTY:

- no hallucinated facts of that type -> score 5
- hallucinated/invented facts -> score 1

Do not penalize the model merely because the expected array is empty.

============================================================
RETRIEVAL-AWARE FAITHFULNESS
============================================================

Pay special attention to the difference between:

A) The retrieved context contains the fact and the model uses it.

B) The retrieved context does NOT contain the fact, but the model
generates it anyway.

Case B should reduce faithfulness and the relevant factual score.

============================================================
EXECUTION
============================================================

Execution success does NOT mean semantic correctness.

Execution failure does NOT automatically mean semantic incorrectness.

Evaluate correctness independently.

============================================================
IMPORTANT
============================================================

Do not give credit for facts merely because you know them from
your own general knowledge.

Do not invent missing Ground Truth.

Do not infer hidden facts.

Return ONLY valid JSON.

No markdown.
No comments.
No explanation outside JSON.

"reasoning" must contain at most TWO short sentences.

============================================================
OUTPUT
============================================================

{{
    "semantic_score": 1,
    "structural_score": 1,
    "faithfulness_score": 1,
    "spatial_score": 1,
    "numerical_score": 1,
    "topological_score": 1,
    "categorical_score": 1,
    "reasoning": "Short explanation."
}}
"""

        invalid_response = {
            "judge_valid": False,
            "semantic_score": None,
            "structural_score": None,
            "faithfulness_score": None,
            "spatial_score": None,
            "numerical_score": None,
            "topological_score": None,
            "categorical_score": None,
            "reasoning": (
                "Judge failed to output valid JSON or valid scores."
            )
        }

        # ====================================================
        # CALL JUDGE
        # ====================================================

        try:

            response = self.judge.invoke(
                prompt
            )

            parsed = self._robust_json_parse(
                response.content
            )

            if not parsed:
                return invalid_response

            # ------------------------------------------------
            # Optional nested hallucination fields
            # ------------------------------------------------

            if "hallucination_subtypes" in parsed:

                subtypes = parsed.pop(
                    "hallucination_subtypes"
                )

                if isinstance(subtypes, dict):
                    parsed.update(subtypes)

            # ------------------------------------------------
            # Validate required scores
            # ------------------------------------------------

            required_keys = [
                "semantic_score",
                "structural_score",
                "faithfulness_score",
                "spatial_score",
                "numerical_score",
                "topological_score",
                "categorical_score"
            ]

            valid = True

            for key in required_keys:

                value = parsed.get(key)

                if not isinstance(
                    value,
                    (int, float)
                ):
                    valid = False
                    break

                if not 1 <= value <= 5:
                    valid = False
                    break

            if not valid:
                return invalid_response

            parsed["judge_valid"] = True

            # Нормализуем reasoning
            parsed["reasoning"] = str(
                parsed.get(
                    "reasoning",
                    ""
                )
            ).strip()

            return parsed

        except Exception as e:

            invalid_response["reasoning"] = (
                f"Judge exception: {str(e)}"
            )

            return invalid_response

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        # ----------------------------------------------------
        # Check files
        # ----------------------------------------------------

        if not os.path.exists(INPUT_PATH):

            logging.error(
                f"❌ Файл не найден: {INPUT_PATH}"
            )

            logging.error(
                "Сначала запусти run_generation.py"
            )

            return

        if not os.path.exists(GROUND_TRUTH_PATH):

            logging.error(
                f"❌ Ground Truth не найден: "
                f"{GROUND_TRUTH_PATH}"
            )

            return

        # ----------------------------------------------------
        # Load data
        # ----------------------------------------------------

        logging.info(
            "📥 Загрузка generation_results.json..."
        )

        with open(
            INPUT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            generation_data = json.load(f)

        logging.info(
            "📥 Загрузка ground_truth.json..."
        )

        with open(
            GROUND_TRUTH_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            ground_truth = json.load(f)

        # ----------------------------------------------------
        # Ground truth index
        # ----------------------------------------------------

        queries_map = {
            str(item.get("id")): item
            for item in ground_truth
        }

        # ----------------------------------------------------
        # Architectures
        # ----------------------------------------------------

        modes = [
            "Baseline",
            "VectorRAG",
            "HydroGraphRAG",
            "HydroGraphRAG_no_CDA",
            "HydroGraphRAG_no_WKT",
            "HydroGraphRAG_no_Template",
            "HydroGraphRAG_no_OOD",
            "HydroGraphRAG_no_Cache",
            "HydroGraphRAG_no_Sandbox"
        ]

        # ----------------------------------------------------
        # Records for CSV
        # ----------------------------------------------------

        evaluation_records = []

        judge_failures = []

        # ====================================================
        # MODELS
        # ====================================================

        for model_data in generation_data:

            model_name = model_data.get(
                "model",
                "unknown"
            )

            logging.info(
                f"\n🧐 Оценка модели: {model_name}"
            )

            metrics = model_data.get(
                "metrics",
                []
            )

            # =================================================
            # QUERIES
            # =================================================

            for item in tqdm(
                metrics,
                desc=f"Judging {model_name}"
            ):

                query_id = str(
                    item.get("query_id")
                )

                gt_item = queries_map.get(
                    query_id,
                    {}
                )

                query = gt_item.get(
                    "query",
                    "Unknown query"
                )

                category = item.get(
                    "category"
                )

                # ---------------------------------------------
                # Anomalous queries
                # ---------------------------------------------

                if category == "anomalous":

                    logging.info(
                        f"⏭️ Skip anomalous query "
                        f"{query_id}"
                    )

                    continue

                # =================================================
                # ARCHITECTURES
                # =================================================

                for mode_name in modes:

                    if mode_name not in item:
                        continue

                    mode_result = item[mode_name]

                    # ---------------------------------------------
                    # Evaluate
                    # ---------------------------------------------

                    scores = self.evaluate(
                        query=query,
                        mode_name=mode_name,
                        mode_result=mode_result,
                        gt_item=gt_item
                    )

                    # ---------------------------------------------
                    # Save scores inside result
                    # ---------------------------------------------

                    mode_result.update(
                        scores
                    )

                    # ---------------------------------------------
                    # Judge failure tracking
                    # ---------------------------------------------

                    if not scores.get(
                        "judge_valid",
                        False
                    ):

                        judge_failures.append({
                            "Model": model_name,
                            "Architecture": mode_name,
                            "Query_ID": query_id,
                            "Reason": scores.get(
                                "reasoning",
                                ""
                            )
                        })

                        continue

                    # ---------------------------------------------
                    # Flat evaluation record
                    # ---------------------------------------------

                    evaluation_records.append({

                        "Model": model_name,

                        "Architecture": mode_name,

                        "Query_ID": query_id,

                        "Semantic_Score": scores.get(
                            "semantic_score"
                        ),

                        "Structural_Score": scores.get(
                            "structural_score"
                        ),

                        "Faithfulness_Overall": scores.get(
                            "faithfulness_score"
                        ),

                        "Spatial": scores.get(
                            "spatial_score"
                        ),

                        "Numeric": scores.get(
                            "numerical_score"
                        ),

                        "Topological": scores.get(
                            "topological_score"
                        ),

                        "Categorical": scores.get(
                            "categorical_score"
                        ),

                        "Execution": mode_result.get(
                            "exec",
                            False
                        ),

                        "Syntax": mode_result.get(
                            "syntax",
                            False
                        ),

                        "Has_Map": mode_result.get(
                            "has_map",
                            False
                        ),

                        "Decision": mode_result.get(
                            "decision",
                            "INVALID"
                        ),

                        "Cache_Hit": mode_result.get(
                            "cache_hit",
                            False
                        ),

                        "Retrieval_Latency": mode_result.get(
                            "retrieval_latency",
                            0
                        ),

                        "Generation_Latency": mode_result.get(
                            "generation_latency",
                            0
                        ),

                        "Total_Latency": mode_result.get(
                            "total_latency",
                            0
                        )
                    })

        # ========================================================
        # SAVE FULL RESULTS
        # ========================================================

        logging.info(
            f"💾 Сохранение результатов: "
            f"{FINAL_OUTPUT_PATH}"
        )

        with open(
            FINAL_OUTPUT_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                generation_data,
                f,
                ensure_ascii=False,
                indent=4
            )

        # ========================================================
        # SAVE DETAILED CSV
        # ========================================================

        if evaluation_records:

            df = pd.DataFrame(
                evaluation_records
            )

            df.to_csv(
                HALLUCINATION_DETAILS_PATH,
                index=False,
                encoding="utf-8-sig"
            )

            logging.info(
                f"📊 Detailed CSV сохранён: "
                f"{HALLUCINATION_DETAILS_PATH}"
            )

            # ----------------------------------------------------
            # Summary
            # ----------------------------------------------------

            summary = (
                df
                .groupby(
                    ["Architecture", "Model"]
                )
                .mean(
                    numeric_only=True
                )
                .round(3)
            )

            summary.to_csv(
                HALLUCINATION_SUMMARY_PATH,
                encoding="utf-8-sig"
            )

            logging.info(
                f"📊 Summary CSV сохранён: "
                f"{HALLUCINATION_SUMMARY_PATH}"
            )

        else:

            logging.warning(
                "⚠️ Нет валидных judge результатов."
            )

        # ========================================================
        # JUDGE FAILURES
        # ========================================================

        if judge_failures:

            failures_path = os.path.join(
                EVAL_DIR,
                "judge_failures.json"
            )

            with open(
                failures_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    judge_failures,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            logging.warning(
                f"⚠️ Judge failures: "
                f"{len(judge_failures)}"
            )

            logging.warning(
                f"Подробности: {failures_path}"
            )

        # ========================================================
        # FINAL LOG
        # ========================================================

        logging.info(
            "\n========================================"
        )

        logging.info(
            "✅ EVALUATION COMPLETE"
        )

        logging.info(
            f"Models evaluated: "
            f"{len(generation_data)}"
        )

        logging.info(
            f"Valid judge records: "
            f"{len(evaluation_records)}"
        )

        logging.info(
            f"Judge failures: "
            f"{len(judge_failures)}"
        )

        logging.info(
            "========================================"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    EvaluationPipeline().run()