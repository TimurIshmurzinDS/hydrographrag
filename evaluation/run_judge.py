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

DETAILED_CSV_PATH = os.path.join(
    EVAL_DIR,
    "hallucination_subtypes_detailed.csv"
)

SUMMARY_CSV_PATH = os.path.join(
    EVAL_DIR,
    "hallucination_subtypes.csv"
)


ABLATION_MODES = [
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


SCORE_KEYS = [
    "semantic_score",
    "structural_score",
    "faithfulness_score",
    "spatial_score",
    "numerical_score",
    "topological_score",
    "categorical_score"
]


# ============================================================
# PIPELINE
# ============================================================

class EvaluationPipeline:

    def __init__(self):

        logging.info(
            f"⚖️ Инициализация независимого судьи: {JUDGE_MODEL}"
        )

        self.judge = ChatOllama(
            model=JUDGE_MODEL,

            # Строгий детерминизм
            temperature=0.0,
            top_p=1.0,
            seed=42,

            # Достаточно большой контекст для
            # Ground Truth + полного ответа модели
            num_ctx=32768
        )


    # ========================================================
    # JSON PARSER
    # ========================================================

    def _robust_json_parse(self, text):

        if not text:
            return None

        try:

            # Удаляем thinking-блоки
            text = re.sub(
                r"<think>.*?</think>",
                "",
                text,
                flags=re.DOTALL | re.IGNORECASE
            ).strip()

            # Сначала пытаемся распарсить весь ответ
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass

            # Если модель добавила текст вокруг JSON,
            # достаём объект.
            match = re.search(
                r"\{.*\}",
                text,
                flags=re.DOTALL
            )

            if not match:
                return None

            json_str = match.group(0)

            # Нормальный JSON
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

            # Fallback для Python-style dict
            try:
                return ast.literal_eval(json_str)
            except Exception:
                return None

        except Exception:

            return None


    # ========================================================
    # SCORE VALIDATION
    # ========================================================

    def _validate_scores(self, parsed):

        if not isinstance(parsed, dict):
            return False

        for key in SCORE_KEYS:

            value = parsed.get(key)

            # bool является subclass int,
            # поэтому отдельно исключаем его.
            if isinstance(value, bool):
                return False

            if not isinstance(value, (int, float)):
                return False

            if not 1 <= value <= 5:
                return False

        return True


    # ========================================================
    # EVALUATION
    # ========================================================

    def evaluate(
        self,
        query,
        raw_response,
        exec_status,
        decision,
        gt_item
    ):

        status_msg = "SUCCESS" if exec_status else "FAILED"

        # ----------------------------------------------------
        # FULL GROUND TRUTH
        # ----------------------------------------------------

        truth_str = f"""
Expected Entities:
{gt_item.get("expected_entities", [])}

Expected Relations:
{gt_item.get("expected_relations", [])}

Expected Triples:
{gt_item.get("expected_triples", [])}

Expected WKT:
{gt_item.get("expected_wkt", [])}

Expected Numeric Values:
{gt_item.get("expected_numeric_facts", [])}

Expected Temporal Facts:
{gt_item.get("expected_temporal_facts", [])}

Expected Categories:
{gt_item.get("expected_categories", [])}

Expected Topology:
{gt_item.get("expected_topology", [])}
"""


        # ----------------------------------------------------
        # JUDGE PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are an independent senior geospatial scientist evaluating
an AI geospatial framework.

Your task is to judge the generated answer against the provided
GROUND TRUTH.

You must evaluate the actual generated response, not whether
the underlying approach "looks reasonable".

============================================================
USER QUERY
============================================================

{query}


============================================================
GROUND TRUTH
============================================================

{truth_str}


============================================================
RUNTIME INFORMATION
============================================================

Model Decision:
{decision}

Execution Status:
{status_msg}


============================================================
GENERATED RAW RESPONSE
============================================================

{raw_response}


============================================================
SCORING
============================================================

Score every dimension from 1 to 5.

1 = completely wrong, fabricated, or contradicts Ground Truth
2 = mostly incorrect, substantial factual errors
3 = partially correct, but contains noticeable errors/omissions
4 = mostly correct, minor errors or omissions
5 = fully correct and faithful to Ground Truth


DIMENSIONS
============================================================

"semantic_score":
Logical coherence and geospatial/domain correctness.

"structure_score":
Whether the response follows the expected response structure,
including explanation and Python code when applicable.

"faithfulness_score":
Overall factual faithfulness to Ground Truth.

"spatial_score":
Correctness of WKT/geometries/coordinates.

"numerical_score":
Correctness of numeric facts such as water levels,
flow rates and measurements.

"topological_score":
Correctness of river connections, upstream/downstream
relationships and graph topology.

"categorical_score":
Correctness of names, classifications, statuses,
regions and other categorical facts.


============================================================
IMPORTANT EMPTY-GROUND-TRUTH RULE
============================================================

If a Ground Truth category is empty:

- If the generated response does NOT invent information
  belonging to that category, give that dimension 5.

- If the generated response invents or hallucinates information
  belonging to that category, give that dimension 1.

Do NOT penalize the model merely because a category is absent
from Ground Truth.

============================================================
IMPORTANT FACTUAL RULES
============================================================

1. Ground Truth is authoritative.

2. Do not assume that information is correct merely because
   it sounds geospatially plausible.

3. Do not give a high score for plausible but unsupported facts.

4. If generated coordinates differ from expected coordinates,
   spatial_score must reflect that difference.

5. If generated numeric values differ from Ground Truth,
   numerical_score must reflect that difference.

6. If generated topology contradicts Ground Truth,
   topological_score must reflect that contradiction.

7. If the model refuses/abstains when the query is answerable,
   this should negatively affect semantic/faithfulness/structural
   quality where appropriate.

8. If the model correctly abstains on an unsupported/anomalous
   query, do not penalize it merely for abstaining.

9. Execution success alone does NOT mean the answer is factually
   correct.

10. Syntax correctness alone does NOT mean the answer is correct.

11. Do not infer correctness from runtime status.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

No markdown.
No code fences.
No explanation outside JSON.

"reasoning" must contain at most 2 short sentences.

Required JSON:

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


        # ----------------------------------------------------
        # INVALID RESULT
        # ----------------------------------------------------

        invalid_response = {

            "judge_valid": False,

            "semantic_score": None,
            "structural_score": None,
            "faithfulness_score": None,
            "spatial_score": None,
            "numerical_score": None,
            "topological_score": None,
            "categorical_score": None,

            "reasoning":
                "Judge failed to output valid JSON or valid scores."
        }


        # ----------------------------------------------------
        # CALL JUDGE
        # ----------------------------------------------------

        try:

            result = self.judge.invoke(prompt)

            parsed = self._robust_json_parse(
                result.content
            )

            if not parsed:
                return invalid_response


            # ------------------------------------------------
            # BACKWARD COMPATIBILITY
            # ------------------------------------------------

            # Если судья случайно вернул:
            #
            # {
            #   "hallucination_subtypes": {
            #       ...
            #   }
            # }
            #
            # разворачиваем структуру.

            if "hallucination_subtypes" in parsed:

                subtypes = parsed.pop(
                    "hallucination_subtypes"
                )

                if isinstance(subtypes, dict):
                    parsed.update(subtypes)


            # ------------------------------------------------
            # NORMALIZE structural_score
            # ------------------------------------------------

            # На случай если модель напишет structure_score
            # вместо structural_score.

            if (
                "structural_score" not in parsed
                and "structure_score" in parsed
            ):
                parsed["structural_score"] = (
                    parsed["structure_score"]
                )


            # ------------------------------------------------
            # VALIDATE
            # ------------------------------------------------

            if not self._validate_scores(parsed):

                return invalid_response


            parsed["judge_valid"] = True

            # Ограничиваем reasoning
            # формально на стороне pipeline.
            reasoning = parsed.get("reasoning", "")

            if not isinstance(reasoning, str):
                reasoning = str(reasoning)

            parsed["reasoning"] = reasoning.strip()


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
        # CHECK INPUTS
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
        # LOAD DATA
        # ----------------------------------------------------

        with open(
            INPUT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            generation_data = json.load(f)


        with open(
            GROUND_TRUTH_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            ground_truth = json.load(f)


        queries_map = {
            str(item.get("id")): item
            for item in ground_truth
        }


        hallucination_records = []


        # ----------------------------------------------------
        # MODELS
        # ----------------------------------------------------

        for model_data in generation_data:

            model_name = model_data.get(
                "model",
                "unknown"
            )

            logging.info(
                f"🧐 Оценка модели: {model_name}"
            )


            metrics = model_data.get(
                "metrics",
                []
            )


            # ------------------------------------------------
            # QUERIES
            # ------------------------------------------------

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


                # ------------------------------------------------
                # OOD / ANOMALOUS
                # ------------------------------------------------

                if item.get("category") == "anomalous":

                    logging.debug(
                        f"Skipping anomalous query {query_id}"
                    )

                    continue


                # ------------------------------------------------
                # ARCHITECTURES
                # ------------------------------------------------

                for mode in ABLATION_MODES:

                    if mode not in item:
                        continue


                    mode_data = item[mode]


                    # IMPORTANT:
                    # Берём именно полный ответ LLM,
                    # сохранённый run_generation.py.

                    raw_response = mode_data.get(
                        "raw_response",
                        ""
                    )

                    exec_status = mode_data.get(
                        "exec",
                        False
                    )

                    decision = mode_data.get(
                        "decision",
                        "INVALID"
                    )


                    # ------------------------------------------------
                    # JUDGE
                    # ------------------------------------------------

                    scores = self.evaluate(
                        query=query,
                        raw_response=raw_response,
                        exec_status=exec_status,
                        decision=decision,
                        gt_item=gt_item
                    )


                    # Добавляем результаты прямо
                    # в generation_results structure.

                    mode_data.update(scores)


                    # ------------------------------------------------
                    # CSV RECORD
                    # ------------------------------------------------

                    if scores.get("judge_valid"):

                        hallucination_records.append({

                            "Model": model_name,

                            "Architecture": mode,

                            "Query_ID": query_id,

                            "Semantic_Score":
                                scores.get(
                                    "semantic_score"
                                ),

                            "Structural_Score":
                                scores.get(
                                    "structural_score"
                                ),

                            "Faithfulness_Overall":
                                scores.get(
                                    "faithfulness_score"
                                ),

                            "Spatial":
                                scores.get(
                                    "spatial_score"
                                ),

                            "Numeric":
                                scores.get(
                                    "numerical_score"
                                ),

                            "Topological":
                                scores.get(
                                    "topological_score"
                                ),

                            "Categorical":
                                scores.get(
                                    "categorical_score"
                                )
                        })


        # ====================================================
        # SAVE FINAL JSON
        # ====================================================

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


        logging.info(
            f"💾 Финальный JSON сохранён: "
            f"{FINAL_OUTPUT_PATH}"
        )


        # ====================================================
        # SAVE DETAILED CSV
        # ====================================================

        if hallucination_records:

            df = pd.DataFrame(
                hallucination_records
            )

            df.to_csv(
                DETAILED_CSV_PATH,
                index=False
            )


            # =================================================
            # SUMMARY
            # =================================================

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
                SUMMARY_CSV_PATH
            )


            logging.info(
                f"📊 Detailed CSV: "
                f"{DETAILED_CSV_PATH}"
            )

            logging.info(
                f"📊 Summary CSV: "
                f"{SUMMARY_CSV_PATH}"
            )

        else:

            logging.warning(
                "⚠️ Не получено ни одной валидной оценки судьи."
            )


        # ====================================================
        # FINAL STATS
        # ====================================================

        total = len(hallucination_records)

        logging.info(
            f"⚖️ Валидных судейских оценок: {total}"
        )

        logging.info(
            "✅ Evaluation Pipeline завершён."
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    EvaluationPipeline().run()
