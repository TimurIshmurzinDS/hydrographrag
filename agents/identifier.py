import json
import logging
import os
import re
from typing import Any, Dict, List

from langchain_ollama import ChatOllama


logger = logging.getLogger(__name__)


class DemandIdentifier:
    """
    Query understanding module for HydroGraphRAG.

    Responsibilities:
      - classify the query into one of four benchmark categories;
      - extract geographic entities;
      - describe the requested output;
      - provide lightweight modeling intent for retrieval.

    This module does not perform graph retrieval or answer generation.
    """

    VALID_CATEGORIES = {
        "explicit",
        "semi-explicit",
        "implicit",
        "anomalous",
    }

    PROMPT_VERSION = "hydrographrag_identifier_v1"

    def __init__(
        self,
        model_name: str = "gemma4:26b",
        num_ctx: int = 8192,
        temperature: float = 0.0,
        top_p: float = 1.0,
        seed: int = 42,
    ):
        self.model_name = model_name
        self.num_ctx = num_ctx
        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed

        self.ollama_base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434",
        )

        self.llm = ChatOllama(
            model=model_name,
            base_url=self.ollama_base_url,
            temperature=temperature,
            top_p=top_p,
            num_ctx=num_ctx,
            seed=seed,
        )

        logger.info(
            "DemandIdentifier initialized | model=%s | base_url=%s",
            self.model_name,
            self.ollama_base_url,
        )

    @staticmethod
    def _clean_model_output(content: Any) -> str:
        """
        Normalize common Ollama/LLM wrappers before JSON parsing.
        """
        if content is None:
            return ""

        text = str(content).strip()

        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        text = (
            text
            .replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )

        return text

    @staticmethod
    def _normalize_entities(value: Any) -> List[str]:
        if value is None:
            return []

        if isinstance(value, str):
            values = [value]

        elif isinstance(value, (list, tuple, set)):
            values = list(value)

        else:
            values = [value]

        entities = []
        seen = set()

        for item in values:
            text = str(item).strip()

            if not text:
                continue

            key = text.casefold()

            if key in seen:
                continue

            seen.add(key)
            entities.append(text)

        return entities

    @classmethod
    def _validate_result(
        cls,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate and normalize the identifier output contract.
        """
        if not isinstance(result, dict):
            raise ValueError(
                "Identifier output must be a JSON object."
            )

        category = str(
            result.get("category", "")
        ).strip().lower()

        if category not in cls.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid query category: {category!r}"
            )

        extracted_inputs = cls._normalize_entities(
            result.get("extracted_inputs")
        )

        target_output = str(
            result.get("target_output", "unknown")
        ).strip()

        modeling_logic = str(
            result.get("modeling_logic", "unknown")
        ).strip()

        return {
            "category": category,
            "extracted_inputs": extracted_inputs,
            "target_output": target_output or "unknown",
            "modeling_logic": modeling_logic or "unknown",
        }

    def _build_prompt(
        self,
        query: str,
    ) -> str:
        return f"""
You are the query-understanding module of HydroGraphRAG,
a hydrology and geospatial reasoning system.

Classify the user query into EXACTLY ONE category:

1. explicit
   Direct lookup, comparison, or analysis involving explicitly
   named hydrological or geographic entities.

2. semi-explicit
   A topological or relational request where the user names an
   entity or region and asks for related entities, locations,
   rivers, stations, or observations.

3. implicit
   A higher-level analytical request requiring multi-hop reasoning,
   connectivity analysis, ecological assessment, risk analysis,
   aggregation, or reasoning across several graph relations.

4. anomalous
   A request outside the hydrology/geospatial domain.

ENTITY EXTRACTION RULES:

- extracted_inputs must contain ONLY concrete geographic or
  hydrological entities relevant for graph retrieval.

- Do not put abstract concepts such as:
  "risk", "statistics", "area", "prediction", "analysis",
  "water level", or "ecology" into extracted_inputs.

- Normalize commonly used Russian geographic names to the English
  labels expected by the knowledge graph when the mapping is clear.

Examples:
  "река Или" -> "Ili River"
  "Алматинская область" -> "Almaty Region"
  "Жетысу" -> "Jetisu Region"
  "Киши Алматы" -> "Kishi Almaty River"

OUTPUT CONTRACT:

Return ONLY one valid JSON object with exactly these fields:

{{
    "category": "explicit | semi-explicit | implicit | anomalous",
    "extracted_inputs": ["entity 1", "entity 2"],
    "target_output": "short description of requested output",
    "modeling_logic": "short description of required retrieval/reasoning"
}}

EXAMPLES:

User:
"Каков текущий уровень воды в реке Или?"

Output:
{{
    "category": "explicit",
    "extracted_inputs": ["Ili River"],
    "target_output": "water level",
    "modeling_logic": "direct lookup"
}}

User:
"Дай информацию на все реки возле Алматы."

Output:
{{
    "category": "semi-explicit",
    "extracted_inputs": ["Almaty City", "Almaty Region"],
    "target_output": "rivers",
    "modeling_logic": "find rivers associated with the requested area"
}}

User:
"Какова общая площадь посевных площадей в регионах,
через которые протекает река Или?"

Output:
{{
    "category": "implicit",
    "extracted_inputs": ["Ili River"],
    "target_output": "arable land area",
    "modeling_logic": "find regions connected to the river and aggregate area"
}}

User:
"{query}"

Return ONLY strict JSON.
""".strip()

    def analyze_query(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """
        Classify and normalize one user query.
        """
        query = str(query).strip()

        if not query:
            raise ValueError("Query must not be empty.")

        prompt = self._build_prompt(query)

        try:
            response = self.llm.invoke(prompt)

            clean_output = self._clean_model_output(
                response.content
            )

            parsed = json.loads(clean_output)

            result = self._validate_result(parsed)

            logger.debug(
                "Query classified as %s with %d extracted entities.",
                result["category"],
                len(result["extracted_inputs"]),
            )

            return result

        except Exception as exc:
            logger.exception(
                "Demand identification failed."
            )

            return {
                "category": "anomalous",
                "extracted_inputs": [],
                "target_output": "unknown",
                "modeling_logic": "identifier_failure",
                "identifier_error": str(exc),
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    identifier = DemandIdentifier()

    test_query = (
        "Проанализируй риск паводка для реки Или "
        "на основе данных постов"
    )

    result = identifier.analyze_query(test_query)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )
