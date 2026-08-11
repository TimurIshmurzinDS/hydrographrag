import logging
import re
from typing import Any, Dict, List, Tuple

from langchain_ollama import ChatOllama


class SolutionPlanner:
    def __init__(
        self,
        model_name: str = "qwen2.5-coder:7b",
        num_ctx: int = 16384,
        max_context_triples: int = 35,
    ):
        self.model_name = model_name
        self.max_context_triples = max_context_triples
        self.shp_path = "data/basin_data.shp"

        self.llm = ChatOllama(
            model=model_name,
            temperature=0.0,
            top_p=1.0,
            num_ctx=num_ctx,
            seed=42,
        )

        logging.info(
            "SolutionPlanner initialized | model=%s | num_ctx=%d | max_triples=%d",
            model_name,
            num_ctx,
            max_context_triples,
        )

    @staticmethod
    def _safe_text(value: Any) -> str:
        if value is None:
            return ""
        return str(value).replace("\x00", " ").strip()

    @staticmethod
    def _escape_python_string(value: Any) -> str:
        text = SolutionPlanner._safe_text(value)
        return (
            text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

    @staticmethod
    def _normalize_entity(value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"\s+", " ", value)
        value = re.sub(r"[.,!?;:()\[\]{}]", "", value)
        return value

    def _extract_context_entities(
        self,
        context_data: Any,
    ) -> List[str]:
        if not isinstance(context_data, list):
            return []

        entities = []

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            source = self._safe_text(triple.get("from"))
            target = self._safe_text(triple.get("to"))

            for value in (source, target):
                if not value:
                    continue

                if (
                    "river" in value.lower()
                    or "lake" in value.lower()
                    or "basin" in value.lower()
                    or "station" in value.lower()
                    or "sensor" in value.lower()
                    or "monitoring" in value.lower()
                ):
                    if value not in entities:
                        entities.append(value)

        return entities

    def _extract_query_entities(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[str]:
        query = self._normalize_entity(user_query)
        context_entities = self._extract_context_entities(context_data)

        matched = []

        for entity in context_entities:
            normalized = self._normalize_entity(entity)

            if normalized and normalized in query:
                matched.append(entity)

        return matched

    def _extract_wkt_points(
        self,
        context_data: Any,
    ) -> List[Dict[str, str]]:
        if not isinstance(context_data, list):
            return []

        points = []

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            if self._safe_text(triple.get("rel")).lower() != "haswkt":
                continue

            name = self._safe_text(triple.get("from"))
            wkt = self._safe_text(triple.get("to"))

            if not name or not wkt:
                continue

            points.append(
                {
                    "name": name,
                    "wkt": wkt,
                }
            )

        return points

    def _select_relevant_wkt(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[Dict[str, str]]:
        points = self._extract_wkt_points(context_data)
        query_entities = self._extract_query_entities(
            user_query,
            context_data,
        )

        if not query_entities:
            return []

        normalized_entities = {
            self._normalize_entity(entity)
            for entity in query_entities
        }

        selected = []

        for point in points:
            normalized_name = self._normalize_entity(point["name"])

            if normalized_name in normalized_entities:
                selected.append(point)

        return selected

    def _select_relevant_triples(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[Dict[str, str]]:
        if not isinstance(context_data, list):
            return []

        query_entities = self._extract_query_entities(
            user_query,
            context_data,
        )

        if not query_entities:
            return []

        normalized_entities = {
            self._normalize_entity(entity)
            for entity in query_entities
        }

        relevant = []

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            if self._safe_text(triple.get("rel")).lower() == "haswkt":
                continue

            source = self._normalize_entity(
                self._safe_text(triple.get("from"))
            )
            target = self._normalize_entity(
                self._safe_text(triple.get("to"))
            )

            if (
                source in normalized_entities
                or target in normalized_entities
            ):
                relevant.append(triple)

        relevant.sort(
            key=lambda x: (
                self._safe_text(x.get("from")).lower(),
                self._safe_text(x.get("rel")).lower(),
                self._safe_text(x.get("to")).lower(),
            )
        )

        return relevant[: self.max_context_triples]

    def _format_triples(
        self,
        triples: List[Dict[str, str]],
    ) -> str:
        if not triples:
            return "No relevant graph triples available."

        lines = []

        for idx, triple in enumerate(triples, start=1):
            source = self._safe_text(triple.get("from"))
            relation = self._safe_text(triple.get("rel"))
            target = self._safe_text(triple.get("to"))

            lines.append(
                f"Triple {idx}: {source} -[{relation}]-> {target}"
            )

        return "\n".join(lines)

    def _format_wkt(
        self,
        points: List[Dict[str, str]],
    ) -> str:
        if not points:
            return "[]"

        lines = ["["]

        for point in points:
            name = self._escape_python_string(point["name"])
            wkt = self._escape_python_string(point["wkt"])

            lines.append(
                f'    {{"name": "{name}", "wkt": "{wkt}"}},'
            )

        lines.append("]")

        return "\n".join(lines)

    def _classify_intent(
        self,
        user_query: str,
    ) -> str:
        query = user_query.lower()

        if any(
            x in query
            for x in [
                "ошиб",
                "error",
                "ошибка",
                "неисправ",
            ]
        ):
            return "sensor_error"

        if any(
            x in query
            for x in [
                "глубин",
                "depth",
            ]
        ):
            return "water_depth"

        if any(
            x in query
            for x in [
                "уровень воды",
                "уровня воды",
                "level",
                "water level",
            ]
        ):
            return "water_level"

        if any(
            x in query
            for x in [
                "статус",
                "состояние",
                "работает",
                "сенсор",
                "датчик",
                "станция",
                "sensor",
                "status",
                "monitoring",
            ]
        ):
            return "monitoring_status"

        if any(
            x in query
            for x in [
                "река",
                "реки",
                "river",
                "бассейн",
                "basin",
                "вод",
                "hydro",
            ]
        ):
            return "hydrology_analysis"

        return "unknown"

    def _is_ood(
        self,
        user_query: str,
    ) -> bool:
        query = user_query.lower()

        domain_terms = [
            "река",
            "реки",
            "реке",
            "вод",
            "уровень",
            "глубина",
            "датчик",
            "сенсор",
            "станция",
            "мониторинг",
            "бассейн",
            "гидролог",
            "river",
            "water",
            "hydrology",
            "hydrological",
            "basin",
            "sensor",
            "monitoring",
            "water level",
            "water depth",
        ]

        return not any(term in query for term in domain_terms)

    def _build_template_code(
        self,
        points: List[Dict[str, str]],
        query_id: str,
    ) -> str:
        safe_query_id = self._escape_python_string(query_id)
        points_literal = self._format_wkt(points)

        return f"""import geopandas as gpd
import folium
from shapely import wkt

basin_data = gpd.read_file(
    r"{self.shp_path}"
).to_crs("EPSG:4326")

centroid = basin_data.geometry.centroid.iloc[0]

m = folium.Map(
    location=[centroid.y, centroid.x],
    tiles="CartoDB positron",
    zoom_start=8,
)

folium.GeoJson(
    basin_data.to_json(),
    style_function=lambda feature: {{
        "fillColor": "green",
        "color": "darkgreen",
        "fillOpacity": 0.2,
    }},
).add_to(m)

points = {points_literal}

for point in points:
    try:
        geom = wkt.loads(point["wkt"])

        if geom.geom_type == "Point":
            folium.Marker(
                location=[geom.y, geom.x],
                popup=point["name"],
            ).add_to(m)

        elif geom.geom_type in ["LineString", "MultiLineString"]:
            folium.GeoJson(
                geom.__geo_interface__,
                name=point["name"],
            ).add_to(m)

        elif geom.geom_type in ["Polygon", "MultiPolygon"]:
            folium.GeoJson(
                geom.__geo_interface__,
                name=point["name"],
            ).add_to(m)

    except Exception:
        pass

m.save("{safe_query_id}.html")"""

    def _build_prompt(
        self,
        user_query: str,
        query_id: str,
        mode_type: str,
        context_data: Any,
        use_ood_rule: bool,
        use_template: bool,
    ) -> str:
        query_entities = self._extract_query_entities(
            user_query,
            context_data,
        )

        relevant_triples = self._select_relevant_triples(
            user_query,
            context_data,
        )

        relevant_wkt = self._select_relevant_wkt(
            user_query,
            context_data,
        )

        intent = self._classify_intent(user_query)

        if mode_type == "baseline":
            graph_context = "No retrieval context."
            wkt_context = "[]"

        elif mode_type == "vector_rag":
            graph_context = self._format_triples(relevant_triples)
            wkt_context = "[]"

        else:
            graph_context = self._format_triples(relevant_triples)
            wkt_context = self._format_wkt(relevant_wkt)

        if use_ood_rule and self._is_ood(user_query):
            return """### Modeling Solution:

ОТКАЗ: Запрос не относится к гидрологии бассейна.

### Implementation Code:

```python
# ОТКАЗ: Запрос не относится к гидрологии бассейна.
```"""

        entities_text = (
            ", ".join(query_entities)
            if query_entities
            else "No matched entities"
        )

        if use_template:
            code = self._build_template_code(
                relevant_wkt,
                query_id,
            )

            code_instruction = f"""
Use exactly this implementation:

```python
{code}

```

Do not add coordinates.
Do not add WKT.
Do not remove retrieved WKT.
Do not use geographic data not present in the supplied context.
"""
        else:
            code_instruction = f"""
Generate Python code from scratch.
The code must:

use geopandas;
use folium;
use {self.shp_path};
convert the basin data to EPSG:4326;
use only the supplied WKT;
never invent coordinates;
gracefully handle missing WKT;
save the result as "{self._escape_python_string(query_id)}.html".
"""

        return f"""

You are a GIS and hydrology solution generator.
Answer only from the supplied evidence.
USER QUERY:
{user_query}
QUERY ID:
{query_id}
QUERY INTENT:
{intent}
MATCHED ENTITIES:
{entities_text}
MODE:
{mode_type}
RELEVANT GRAPH FACTS:
{graph_context}
RELEVANT WKT:
{wkt_context}
RULES:

Never invent geographic entities.
Never invent numerical hydrological values.
Never invent dates or temporal facts.
Never invent coordinates.
Never invent WKT.
Never use general knowledge as retrieved evidence.
Only WKT listed under RELEVANT WKT may be used in Python.
WKT must remain exactly unchanged.
If a requested numerical fact is absent, explicitly say that it is unavailable.
Having WKT does not imply that a water-level value, sensor status, depth, or measurement exists.
Do not claim that a measurement was obtained when the context contains only geometry.
If multiple entities are present in the query, handle all matched entities.
If no relevant WKT exists, create the basin map without fabricated geometries.
The explanation must be in the same language as the user query.
The response must contain exactly two sections.
The first section must explain what is supported and what is unavailable.
The second section must contain executable Python code.
{code_instruction}
Return exactly:

### Modeling Solution:

[Your explanation here]

### Implementation Code:

    [Your code here]
    """

    def generate_response(
        self,
        user_query: str,
        query_id: str,
        mode_type: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> str:
        if mode_type not in {
            "baseline",
            "vector_rag",
            "hydrographrag",
        }:
            raise ValueError(
                f"Unknown generation mode: {mode_type}"
            )

        prompt = self._build_prompt(
            user_query=user_query,
            query_id=query_id,
            mode_type=mode_type,
            context_data=context_data,
            use_ood_rule=use_ood_rule,
            use_template=use_template,
        )

        response = self.llm.invoke(prompt)

        return response.content.strip()

    def generate(
        self,
        mode: str,
        user_query: str,
        query_id: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> str:
        return self.generate_response(
            user_query=user_query,
            query_id=query_id,
            mode_type=mode,
            context_data=context_data,
            use_ood_rule=use_ood_rule,
            use_template=use_template,
        )
