import hashlib
import json
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from langchain_ollama import ChatOllama


class SolutionPlanner:
    """
    Final Solution Planner for the revised HydroGraphRAG evaluation.

    Main responsibilities:
    ------------------------------------------------------------
    1. Build one controlled generation prompt for:
       - Baseline
       - VectorRAG
       - HydroGraphRAG

    2. Enforce the same output contract:
       decision: ANSWER | ABSTAIN
       abstain_reason: ...

       ### Modeling Solution:
       ...

       ### Implementation Code:
       ...

    3. Never invent:
       - coordinates
       - WKT
       - numerical hydrological measurements
       - temporal observations
       - graph relations

    4. Support GraphDB WKT predicates:
       - geo:asWKT
       - asWKT
       - hasWKT

    5. Preserve retrieved multi-hop evidence instead of keeping
       only direct 1-hop triples.

    6. Preserve VectorRAG string context.

    7. Expose exact final prompt and SHA256 for reproducibility.

    IMPORTANT:
    ------------------------------------------------------------
    OOD abstention is a semantic decision.

    Execution failure is NOT abstention.
    Generation failure is NOT abstention.

    These distinctions must be preserved in run_generation.py.
    """

    SYSTEM_PROMPT_VERSION = "hydrographrag_system_v3"
    TEMPLATE_VERSION = "geopandas_folium_template_v3"
    ABSTENTION_POLICY_VERSION = "ood_policy_v2"

    VALID_MODES = {
        "baseline",
        "vector_rag",
        "hydrographrag",
    }

    WKT_RELATIONS = {
        "haswkt",
        "aswkt",
    }

    LABEL_RELATIONS = {
        "label",
        "name",
        "post_name",
        "postname",
    }

    # Relations whose targets are usually literals rather than
    # graph entities. They should not normally expand BFS traversal.
    LITERAL_RELATION_HINTS = {
        "hasresult",
        "resulttime",
        "hastime",
        "date_water_level_value",
        "water_level_value",
        "water_level_valuecm",
        "water_consumption_value",
        "water_consumption_valuem³s",
        "population_region_2022",
        "haspopulation",
        "width",
        "length_km",
        "basin_are_km²",
        "volume_m³s",
        "concentration_2022",
        "unit",
        "attribute",
        "post_code",
    }

    def __init__(
        self,
        model_name: str = "qwen2.5-coder:7b",
        num_ctx: int = 8192,
        max_context_triples: int = 35,
        max_wkt_geometries: int = 20,
        max_relevance_hops: int = 3,
        temperature: float = 0.0,
        top_p: float = 1.0,
        seed: int = 42,
    ):
        self.model_name = model_name
        self.num_ctx = num_ctx
        self.max_context_triples = max_context_triples
        self.max_wkt_geometries = max_wkt_geometries
        self.max_relevance_hops = max_relevance_hops

        self.temperature = temperature
        self.top_p = top_p
        self.seed = seed

        self.shp_path = "data/basin_data.shp"

        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            num_ctx=num_ctx,
            seed=seed,
        )

        # Useful for run_generation.py after its next revision.
        self.last_prompt: Optional[str] = None
        self.last_prompt_sha256: Optional[str] = None
        self.last_prompt_metadata: Dict[str, Any] = {}

        logging.info(
            (
                "SolutionPlanner initialized | "
                "model=%s | num_ctx=%d | "
                "max_triples=%d | max_wkt=%d | max_hops=%d"
            ),
            model_name,
            num_ctx,
            max_context_triples,
            max_wkt_geometries,
            max_relevance_hops,
        )

    # ============================================================
    # BASIC NORMALIZATION
    # ============================================================

    @staticmethod
    def _safe_text(value: Any) -> str:
        if value is None:
            return ""

        return (
            str(value)
            .replace("\x00", " ")
            .strip()
        )

    @staticmethod
    def _escape_python_string(value: Any) -> str:
        text = SolutionPlanner._safe_text(value)

        return (
            text
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

    @staticmethod
    def _uri_local_name(value: Any) -> str:
        """
        Converts values such as:

            http://...#asWKT
            geo:asWKT
            wr_kz:Post_name
            <http://.../River>

        to their local name.
        """

        text = SolutionPlanner._safe_text(value)

        if not text:
            return ""

        text = text.strip("<>")

        if "#" in text:
            text = text.rsplit("#", 1)[-1]

        elif "/" in text:
            text = text.rsplit("/", 1)[-1]

        if ":" in text:
            text = text.rsplit(":", 1)[-1]

        return text.strip()

    @classmethod
    def _normalize_relation(cls, value: Any) -> str:
        local = cls._uri_local_name(value)

        local = (
            local
            .strip()
            .lower()
            .replace(" ", "_")
        )

        return local

    @classmethod
    def _is_wkt_relation(cls, relation: Any) -> bool:
        normalized = cls._normalize_relation(relation)

        return normalized in cls.WKT_RELATIONS

    @classmethod
    def _is_label_relation(cls, relation: Any) -> bool:
        normalized = cls._normalize_relation(relation)

        return normalized in cls.LABEL_RELATIONS

    @staticmethod
    def _normalize_entity(value: Any) -> str:
        """
        Normalizes both readable labels and RDF-like local names.

        Examples:
            Ili River        -> ili river
            sw:IliRiver      -> ili river
            Kishi_Almaty     -> kishi almaty
        """

        text = SolutionPlanner._safe_text(value)

        if not text:
            return ""

        text = text.strip("<>")

        # URI local part
        if "#" in text:
            text = text.rsplit("#", 1)[-1]

        elif (
            text.startswith("http://")
            or text.startswith("https://")
        ):
            text = text.rstrip("/").rsplit("/", 1)[-1]

        # namespace
        if ":" in text and "://" not in text:
            text = text.rsplit(":", 1)[-1]

        # Split camel case:
        # IliRiver -> Ili River
        text = re.sub(
            r"(?<=[a-z0-9])(?=[A-Z])",
            " ",
            text,
        )

        text = text.replace("_", " ")
        text = text.replace("-", " ")

        text = text.lower()

        text = re.sub(
            r"[.,!?;:()\[\]{}\"']",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # ============================================================
    # TRIPLE ACCESS
    # ============================================================

    def _get_triple_fields(
        self,
        triple: Dict[str, Any],
    ) -> Tuple[str, str, str]:
        """
        Supports both project-native:

            from / rel / to

        and generic:

            source / relation / target
        """

        source = self._safe_text(
            triple.get(
                "from",
                triple.get("source", ""),
            )
        )

        relation = self._safe_text(
            triple.get(
                "rel",
                triple.get(
                    "relation",
                    triple.get("predicate", ""),
                ),
            )
        )

        target = self._safe_text(
            triple.get(
                "to",
                triple.get(
                    "target",
                    triple.get("object", ""),
                ),
            )
        )

        return source, relation, target

    # ============================================================
    # LITERAL DETECTION
    # ============================================================

    @staticmethod
    def _looks_like_wkt(value: Any) -> bool:
        text = SolutionPlanner._safe_text(value).upper()

        geometry_types = (
            "POINT",
            "LINESTRING",
            "POLYGON",
            "MULTIPOINT",
            "MULTILINESTRING",
            "MULTIPOLYGON",
            "GEOMETRYCOLLECTION",
        )

        return any(
            text.startswith(g)
            for g in geometry_types
        )

    @staticmethod
    def _looks_like_number(value: Any) -> bool:
        text = SolutionPlanner._safe_text(value)

        if not text:
            return False

        return bool(
            re.fullmatch(
                r"[-+]?\d+(?:[.,]\d+)?(?:\s*[A-Za-zА-Яа-я/%³²]+)?",
                text,
            )
        )

    @staticmethod
    def _looks_like_date(value: Any) -> bool:
        text = SolutionPlanner._safe_text(value)

        patterns = [
            r"\d{4}-\d{1,2}-\d{1,2}",
            r"\d{1,2}[./-]\d{1,2}[./-]\d{4}",
            r"\d{4}",
        ]

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )

    def _looks_like_entity_node(
        self,
        value: Any,
    ) -> bool:
        text = self._safe_text(value)

        if not text:
            return False

        if self._looks_like_wkt(text):
            return False

        if self._looks_like_number(text):
            return False

        if self._looks_like_date(text):
            return False

        if len(text) > 250:
            return False

        return bool(
            re.search(
                r"[A-Za-zА-Яа-я]",
                text,
            )
        )

    # ============================================================
    # CONTEXT ENTITY EXTRACTION
    # ============================================================

    def _extract_context_entities(
        self,
        context_data: Any,
    ) -> List[str]:
        """
        Extract possible entity nodes from graph context.

        We intentionally do not restrict this to only words such as
        River/Lake/Station because intermediate Observation nodes are
        necessary for multi-hop traversal and WKT association.
        """

        if not isinstance(context_data, list):
            return []

        result: List[str] = []
        seen: Set[str] = set()

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            source, relation, target = (
                self._get_triple_fields(triple)
            )

            for value in (source, target):
                if not self._looks_like_entity_node(value):
                    continue

                normalized = self._normalize_entity(value)

                if not normalized:
                    continue

                if normalized in seen:
                    continue

                seen.add(normalized)
                result.append(value)

        return result

    def _extract_query_entities(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[str]:
        """
        Finds context entities explicitly mentioned in the query.

        Query text may be Russian while graph entity labels are English.
        This is still sufficient for benchmark queries such as:

            "... Ili River"
            "... Karatal River"
        """

        query_normalized = self._normalize_entity(
            user_query
        )

        candidates = self._extract_context_entities(
            context_data
        )

        # Longer entities first to avoid matching a shorter nested name.
        candidates = sorted(
            candidates,
            key=lambda x: len(
                self._normalize_entity(x)
            ),
            reverse=True,
        )

        matched: List[str] = []
        matched_normalized: Set[str] = set()

        for candidate in candidates:
            normalized = self._normalize_entity(
                candidate
            )

            if not normalized:
                continue

            if normalized not in query_normalized:
                continue

            if normalized in matched_normalized:
                continue

            matched.append(candidate)
            matched_normalized.add(normalized)

        return matched

    # ============================================================
    # GRAPH RELEVANCE / MULTI-HOP EVIDENCE
    # ============================================================

    def _reachable_nodes(
        self,
        user_query: str,
        context_data: Any,
    ) -> Set[str]:
        """
        Controlled BFS over already retrieved context.

        This is NOT ontology retrieval itself.
        GraphRetriever has already performed retrieval.

        This method only prevents SolutionPlanner from discarding
        useful intermediate nodes such as:

            River
              -> Observation
              -> Post_name
              -> asWKT

        which the previous 1-hop filter lost.
        """

        if not isinstance(context_data, list):
            return set()

        query_entities = self._extract_query_entities(
            user_query,
            context_data,
        )

        # For implicit queries no explicit graph entity may be present
        # in the natural-language query. In that case the retrieved
        # subgraph itself is already the evidence package and we keep
        # all entity nodes reachable inside it.
        if not query_entities:
            nodes: Set[str] = set()

            for triple in context_data:
                if not isinstance(triple, dict):
                    continue

                source, relation, target = (
                    self._get_triple_fields(triple)
                )

                if self._looks_like_entity_node(source):
                    nodes.add(
                        self._normalize_entity(source)
                    )

                if self._looks_like_entity_node(target):
                    nodes.add(
                        self._normalize_entity(target)
                    )

            return nodes

        reached = {
            self._normalize_entity(entity)
            for entity in query_entities
            if self._normalize_entity(entity)
        }

        frontier = set(reached)

        for _ in range(self.max_relevance_hops):
            if not frontier:
                break

            next_frontier: Set[str] = set()

            for triple in context_data:
                if not isinstance(triple, dict):
                    continue

                source, relation, target = (
                    self._get_triple_fields(triple)
                )

                if self._is_wkt_relation(relation):
                    continue

                source_n = self._normalize_entity(source)
                target_n = self._normalize_entity(target)

                source_is_entity = (
                    self._looks_like_entity_node(source)
                )

                target_is_entity = (
                    self._looks_like_entity_node(target)
                )

                if (
                    source_n in frontier
                    and target_is_entity
                    and target_n
                    and target_n not in reached
                ):
                    next_frontier.add(target_n)

                if (
                    target_n in frontier
                    and source_is_entity
                    and source_n
                    and source_n not in reached
                ):
                    next_frontier.add(source_n)

            reached.update(next_frontier)
            frontier = next_frontier

        return reached

    def _select_relevant_triples(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[Dict[str, Any]]:
        """
        Selects graph evidence using bounded connectivity instead
        of the previous strict direct-entity-only filter.

        WKT triples are excluded here and supplied separately.
        """

        if not isinstance(context_data, list):
            return []

        reached = self._reachable_nodes(
            user_query,
            context_data,
        )

        relevant: List[Dict[str, Any]] = []

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            source, relation, target = (
                self._get_triple_fields(triple)
            )

            if self._is_wkt_relation(relation):
                continue

            source_n = self._normalize_entity(source)
            target_n = self._normalize_entity(target)

            # If no meaningful connectivity information exists,
            # preserve retrieved evidence because GraphRetriever
            # already selected this subgraph.
            if not reached:
                relevant.append(triple)
                continue

            if (
                source_n in reached
                or target_n in reached
            ):
                relevant.append(triple)

        # Stable deterministic order.
        relevant.sort(
            key=lambda triple: (
                self._safe_text(
                    self._get_triple_fields(triple)[0]
                ).lower(),
                self._safe_text(
                    self._get_triple_fields(triple)[1]
                ).lower(),
                self._safe_text(
                    self._get_triple_fields(triple)[2]
                ).lower(),
            )
        )

        return relevant[
            : self.max_context_triples
        ]

    # ============================================================
    # WKT EXTRACTION
    # ============================================================

    def _build_subject_label_map(
        self,
        context_data: Any,
    ) -> Dict[str, str]:
        """
        Maps graph subjects such as Observation_14 to retrieved
        human-readable labels such as:

            Dobyn pier
            Talgar city
            (near Ili)

        Nothing external is invented.
        """

        if not isinstance(context_data, list):
            return {}

        labels: Dict[str, str] = {}

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            source, relation, target = (
                self._get_triple_fields(triple)
            )

            if not self._is_label_relation(relation):
                continue

            if not source or not target:
                continue

            labels[
                self._normalize_entity(source)
            ] = target

        return labels

    @staticmethod
    def _clean_wkt_literal(value: Any) -> str:
        """
        Handles both plain WKT:

            POINT(80.046 43.4)

        and RDF lexical strings such as:

            "POINT(80.046 43.4)"^^<...wktLiteral>

        The inner WKT itself is not modified.
        """

        text = SolutionPlanner._safe_text(
            value
        )

        if not text:
            return ""

        datatype_match = re.match(
            r'^["\'](.+?)["\']\^\^',
            text,
            flags=re.DOTALL,
        )

        if datatype_match:
            return datatype_match.group(1)

        if (
            len(text) >= 2
            and text[0] in {"'", '"'}
            and text[-1] == text[0]
        ):
            return text[1:-1]

        return text

    def _extract_wkt_geometries(
        self,
        context_data: Any,
    ) -> List[Dict[str, str]]:
        if not isinstance(context_data, list):
            return []

        labels = self._build_subject_label_map(
            context_data
        )

        geometries: List[Dict[str, str]] = []
        seen: Set[Tuple[str, str]] = set()

        for triple in context_data:
            if not isinstance(triple, dict):
                continue

            source, relation, target = (
                self._get_triple_fields(triple)
            )

            if not self._is_wkt_relation(relation):
                continue

            wkt_text = self._clean_wkt_literal(
                target
            )

            if not source or not wkt_text:
                continue

            if not self._looks_like_wkt(wkt_text):
                logging.warning(
                    "Ignoring malformed WKT candidate | source=%s | value=%s",
                    source,
                    target,
                )
                continue

            source_normalized = (
                self._normalize_entity(source)
            )

            display_name = labels.get(
                source_normalized,
                source,
            )

            key = (
                self._normalize_entity(
                    display_name
                ),
                wkt_text,
            )

            if key in seen:
                continue

            seen.add(key)

            geometries.append(
                {
                    "source": source,
                    "name": display_name,
                    "wkt": wkt_text,
                }
            )

        return geometries

    def _select_relevant_wkt(
        self,
        user_query: str,
        context_data: Any,
    ) -> List[Dict[str, str]]:
        """
        Associates WKT with graph nodes reachable from the query
        entity rather than requiring:

            query entity == WKT subject

        This is necessary because the real GraphDB stores WKT on
        observation/location nodes.
        """

        geometries = self._extract_wkt_geometries(
            context_data
        )

        if not geometries:
            return []

        reached = self._reachable_nodes(
            user_query,
            context_data,
        )

        selected: List[Dict[str, str]] = []

        for geometry in geometries:
            source_n = self._normalize_entity(
                geometry["source"]
            )

            if reached and source_n not in reached:
                continue

            selected.append(
                {
                    "name": geometry["name"],
                    "wkt": geometry["wkt"],
                }
            )

            if (
                len(selected)
                >= self.max_wkt_geometries
            ):
                break

        # For graph retrieval without explicit lexical query
        # anchors, reached contains the retrieved entity region.
        # As a final fallback, preserve retrieved WKT rather than
        # silently dropping spatial evidence.
        if not selected:
            for geometry in geometries[
                : self.max_wkt_geometries
            ]:
                selected.append(
                    {
                        "name": geometry["name"],
                        "wkt": geometry["wkt"],
                    }
                )

        return selected

    # ============================================================
    # FORMATTING
    # ============================================================

    def _format_triples(
        self,
        triples: List[Dict[str, Any]],
    ) -> str:
        if not triples:
            return (
                "No relevant graph facts were "
                "available in the retrieved evidence."
            )

        lines: List[str] = []

        for idx, triple in enumerate(
            triples,
            start=1,
        ):
            source, relation, target = (
                self._get_triple_fields(triple)
            )

            lines.append(
                (
                    f"Triple {idx}: "
                    f"{source} "
                    f"-[{relation}]-> "
                    f"{target}"
                )
            )

        return "\n".join(lines)

    def _format_wkt(
        self,
        geometries: List[Dict[str, str]],
    ) -> str:
        if not geometries:
            return "[]"

        lines = ["["]

        for item in geometries:
            name = self._escape_python_string(
                item["name"]
            )

            wkt_text = self._escape_python_string(
                item["wkt"]
            )

            lines.append(
                (
                    '    {'
                    f'"name": "{name}", '
                    f'"wkt": "{wkt_text}"'
                    "},"
                )
            )

        lines.append("]")

        return "\n".join(lines)

    def _format_vector_context(
        self,
        context_data: Any,
    ) -> str:
        """
        VectorRAG in current run_generation.py sends a STRING:

            Entity: ...
            Entity: ...

        Previous planner accidentally discarded it because it expected
        a list of graph triples.
        """

        if context_data is None:
            return (
                "No retrieved evidence was supplied."
            )

        if isinstance(context_data, str):
            text = context_data.strip()

            return (
                text
                if text
                else "No retrieved evidence was supplied."
            )

        if isinstance(context_data, list):
            return self._format_triples(
                [
                    triple
                    for triple in context_data
                    if isinstance(triple, dict)
                ]
            )

        return self._safe_text(
            context_data
        )

    # ============================================================
    # INTENT
    # ============================================================

    def _classify_intent(
        self,
        user_query: str,
    ) -> str:
        """
        Domain intent != cognitive-demand category.

        This function describes what information the user requests.
        Explicit / Semi-explicit / Implicit / OOD remain separate
        concepts handled by the CDA/evaluation layer.
        """

        query = user_query.lower()

        if any(
            token in query
            for token in [
                "ошиб",
                "error",
                "неисправ",
                "failure",
                "fault",
            ]
        ):
            return "sensor_error"

        if any(
            token in query
            for token in [
                "глубин",
                "water depth",
                "depth",
            ]
        ):
            return "water_depth"

        if any(
            token in query
            for token in [
                "уровень воды",
                "уровня воды",
                "water level",
            ]
        ):
            return "water_level"

        if any(
            token in query
            for token in [
                "расход",
                "discharge",
                "flow rate",
                "streamflow",
            ]
        ):
            return "water_discharge"

        if any(
            token in query
            for token in [
                "качество воды",
                "water quality",
                "концентрац",
                "pollut",
                "chemical",
            ]
        ):
            return "water_quality"

        if any(
            token in query
            for token in [
                "павод",
                "наводнен",
                "flood",
            ]
        ):
            return "flood_analysis"

        if any(
            token in query
            for token in [
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
            token in query
            for token in [
                "река",
                "river",
                "бассейн",
                "basin",
                "гидролог",
                "hydrolog",
                "water",
                "вод",
            ]
        ):
            return "hydrology_analysis"

        return "unknown"

    # ============================================================
    # TEMPLATE
    # ============================================================

    def _build_template_code(
        self,
        geometries: List[Dict[str, str]],
        query_id: str,
    ) -> str:
        """
        Fixed GIS execution skeleton shared by:
            Baseline
            VectorRAG
            HydroGraphRAG

        The only query-dependent spatial content is retrieved WKT.
        """

        safe_query_id = (
            self._escape_python_string(
                query_id
            )
        )

        geometries_literal = (
            self._format_wkt(
                geometries
            )
        )

        return f'''import logging

import folium
import geopandas as gpd
from shapely import wkt


SHAPEFILE_PATH = r"{self.shp_path}"
OUTPUT_HTML = "{safe_query_id}.html"


basin_data = gpd.read_file(
    SHAPEFILE_PATH
)

if basin_data.empty:
    raise ValueError(
        "Basin shapefile contains no geometries."
    )

if basin_data.crs is None:
    raise ValueError(
        "Basin shapefile CRS is undefined."
    )

basin_data = basin_data.to_crs(
    "EPSG:4326"
)

minx, miny, maxx, maxy = (
    basin_data.total_bounds
)

map_center = [
    (miny + maxy) / 2.0,
    (minx + maxx) / 2.0,
]

m = folium.Map(
    location=map_center,
    tiles="CartoDB positron",
    zoom_start=8,
)

folium.GeoJson(
    basin_data.to_json(),
    name="Basin boundary",
    style_function=lambda feature: {{
        "fillColor": "green",
        "color": "darkgreen",
        "fillOpacity": 0.2,
    }},
).add_to(m)


retrieved_geometries = {geometries_literal}


for item in retrieved_geometries:
    try:
        geometry = wkt.loads(
            item["wkt"]
        )

        geometry_type = (
            geometry.geom_type
        )

        if geometry_type == "Point":
            folium.Marker(
                location=[
                    geometry.y,
                    geometry.x,
                ],
                popup=item["name"],
            ).add_to(m)

        elif geometry_type in {{
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
        }}:
            folium.GeoJson(
                geometry.__geo_interface__,
                name=item["name"],
            ).add_to(m)

        else:
            logging.warning(
                "Unsupported geometry type for %s: %s",
                item["name"],
                geometry_type,
            )

    except Exception as exc:
        logging.warning(
            "Could not render retrieved WKT for %s: %s",
            item.get("name", "unknown"),
            exc,
        )


folium.LayerControl().add_to(m)

m.save(
    OUTPUT_HTML
)
'''

    # ============================================================
    # PROMPT HASH
    # ============================================================

    @staticmethod
    def _sha256_text(
        text: str,
    ) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    # ============================================================
    # PROMPT
    # ============================================================

    def _build_prompt(
        self,
        user_query: str,
        query_id: str,
        mode_type: str,
        context_data: Any,
        use_ood_rule: bool,
        use_template: bool,
    ) -> str:
        """
        Builds the exact prompt given to the generator model.

        Baseline / VectorRAG / HydroGraphRAG share:
            - output contract
            - abstention policy
            - factual safety rules
            - code-template policy

        Their principal difference is the evidence provided.
        """

        if mode_type not in self.VALID_MODES:
            raise ValueError(
                f"Unknown generation mode: {mode_type}"
            )

        intent = self._classify_intent(
            user_query
        )

        # --------------------------------------------------------
        # BASELINE
        # --------------------------------------------------------

        if mode_type == "baseline":
            evidence_context = (
                "No external retrieval evidence was supplied."
            )

            relevant_wkt: List[
                Dict[str, str]
            ] = []

            matched_entities: List[str] = []

        # --------------------------------------------------------
        # VECTOR RAG
        # --------------------------------------------------------

        elif mode_type == "vector_rag":
            evidence_context = (
                self._format_vector_context(
                    context_data
                )
            )

            # Flat vector retrieval does not provide trusted
            # ontology WKT in this experiment.
            relevant_wkt = []

            matched_entities = []

        # --------------------------------------------------------
        # HYDROGRAPH RAG
        # --------------------------------------------------------

        else:
            relevant_triples = (
                self._select_relevant_triples(
                    user_query,
                    context_data,
                )
            )

            relevant_wkt = (
                self._select_relevant_wkt(
                    user_query,
                    context_data,
                )
            )

            matched_entities = (
                self._extract_query_entities(
                    user_query,
                    context_data,
                )
            )

            evidence_context = (
                self._format_triples(
                    relevant_triples
                )
            )

        entities_text = (
            ", ".join(matched_entities)
            if matched_entities
            else "No explicit entity match."
        )

        wkt_context = (
            self._format_wkt(
                relevant_wkt
            )
        )

        # --------------------------------------------------------
        # OOD POLICY
        # --------------------------------------------------------

        if use_ood_rule:
            decision_policy = """
OOD / ABSTENTION POLICY:

You MUST make a semantic domain decision before answering.

Return:

decision: ABSTAIN

ONLY when the PRIMARY requested task is outside the supported
hydrology/GIS analytical domain.

A request is still out-of-domain when it merely mentions a river,
basin, coordinate, water level, or hydrological object as incidental
input for an unrelated primary objective.

Examples of unrelated objectives include non-hydrological tasks such
as recipes, jokes, cryptocurrency prediction, astronomy calculations,
or other tasks whose requested outcome is not hydrological/GIS
analysis.

IMPORTANT:

Do NOT abstain merely because a valid hydrological query requests a
measurement, date, relationship, or value that is absent from the
evidence.

For an in-domain but unsupported request:

decision: ANSWER

and explicitly state that the requested fact is unavailable in the
supplied evidence.
""".strip()

        else:
            decision_policy = """
OOD / ABSTENTION POLICY:

OOD rejection is disabled for this ablation.

You MUST return:

decision: ANSWER

Do not return ABSTAIN.
""".strip()

        # --------------------------------------------------------
        # CODE POLICY
        # --------------------------------------------------------

        if use_template:
            template_code = (
                self._build_template_code(
                    relevant_wkt,
                    query_id,
                )
            )

            code_instruction = f"""
FIXED CODE TEMPLATE:

Use the following implementation skeleton exactly.

Do not replace the retrieved WKT.
Do not add coordinates.
Do not add WKT.
Do not remove supplied WKT.
Do not insert geographic data from model memory.

```python
{template_code}
```
""".strip()

        else:
            code_instruction = f"""
CODE GENERATION ABLATION:

The fixed code template is disabled.

Generate Python code from scratch.

The code MUST:

- use geopandas;
- use folium;
- load r"{self.shp_path}";
- convert basin data to EPSG:4326;
- use only WKT explicitly supplied under TRUSTED WKT;
- never invent coordinates;
- never invent WKT;
- gracefully handle the absence of WKT;
- save exactly "{self._escape_python_string(query_id)}.html".
""".strip()

        # --------------------------------------------------------
        # FINAL PROMPT
        # --------------------------------------------------------

        prompt = f"""
You are a controlled GIS and hydrology solution generator used in a
scientific evaluation.

Your objective is to answer the user's hydrological/GIS request while
strictly separating supported evidence from unavailable information.

============================================================
OUTPUT CONTRACT
============================================================

Your response MUST begin with exactly these two metadata lines:

decision: ANSWER
abstain_reason: NONE

OR:

decision: ABSTAIN
abstain_reason: <SHORT_REASON>

After those metadata lines, return exactly these two sections:

### Modeling Solution:

<explanation>

### Implementation Code:

```python
<code>
```

Do not create any additional sections.

============================================================
USER QUERY
============================================================

{user_query}

============================================================
QUERY ID
============================================================

{query_id}

============================================================
DOMAIN INTENT
============================================================

{intent}

============================================================
EXPLICITLY MATCHED GRAPH ENTITIES
============================================================

{entities_text}

============================================================
RETRIEVED EVIDENCE
============================================================

{evidence_context}

============================================================
TRUSTED WKT
============================================================

{wkt_context}

============================================================
DECISION POLICY
============================================================

{decision_policy}

============================================================
FACTUAL GROUNDING RULES
============================================================

1. Never invent geographic coordinates.

2. Never invent WKT.

3. Never alter a supplied WKT literal.

4. Never invent query-specific hydrological measurements such as:
   - water level;
   - discharge;
   - depth;
   - concentration;
   - sensor readings.

5. Never invent dates, years, observation timestamps, historical
   records, forecasts, or temporal measurements.

6. Never invent graph topology or relations such as:
   - upstream/downstream;
   - tributary relationships;
   - located-in relationships;
   - station-to-river relationships.

7. Never claim that WKT geometry proves:
   - current water level;
   - sensor status;
   - water depth;
   - discharge;
   - measurement availability.

8. Retrieved geometry is spatial evidence only.

9. If a requested fact is absent from the supplied evidence, explicitly
   state that the requested fact is unavailable in the supplied
   evidence.

10. Do not silently substitute a different measurement or entity.

11. If multiple requested entities are supported by the evidence,
    address all of them.

12. If no trusted WKT exists, the generated GIS code may render only
    the basin shapefile.

13. General hydrological knowledge may be used only for neutral
    explanatory background. It must never be presented as a retrieved,
    measured, observed, or query-specific fact.

14. The Modeling Solution must use the same natural language as the
    user's query.

15. The Python implementation must use only spatial data allowed by
    this prompt.

============================================================
IMPLEMENTATION POLICY
============================================================

{code_instruction}

============================================================
FINAL INSTRUCTION
============================================================

First make the ANSWER/ABSTAIN decision according to the decision policy.

For ANSWER:

decision: ANSWER
abstain_reason: NONE

Then provide both required sections.

For ABSTAIN:

decision: ABSTAIN
abstain_reason: OUT_OF_DOMAIN

The Modeling Solution must briefly explain that the primary task is
outside the supported hydrology/GIS analytical domain.

The Implementation Code section must contain only:

```python
# No code generated because the request was rejected as out-of-domain.
```

Return no text outside the required format.
""".strip()

        return prompt

    # ============================================================
    # PUBLIC PROMPT API
    # ============================================================

    def build_prompt(
        self,
        user_query: str,
        query_id: str,
        mode: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> str:
        """
        Public method for reproducible experiment logging.
        """

        prompt = self._build_prompt(
            user_query=user_query,
            query_id=query_id,
            mode_type=mode,
            context_data=context_data,
            use_ood_rule=use_ood_rule,
            use_template=use_template,
        )

        return prompt

    # ============================================================
    # GENERATION
    # ============================================================

    def generate_response(
        self,
        user_query: str,
        query_id: str,
        mode_type: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> str:
        if mode_type not in self.VALID_MODES:
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

        prompt_sha256 = self._sha256_text(
            prompt
        )

        self.last_prompt = prompt
        self.last_prompt_sha256 = (
            prompt_sha256
        )

        self.last_prompt_metadata = {
            "prompt_sha256": prompt_sha256,
            "system_prompt_version": (
                self.SYSTEM_PROMPT_VERSION
            ),
            "template_version": (
                self.TEMPLATE_VERSION
                if use_template
                else "disabled"
            ),
            "abstention_policy_version": (
                self.ABSTENTION_POLICY_VERSION
                if use_ood_rule
                else "disabled"
            ),
            "model": self.model_name,
            "num_ctx": self.num_ctx,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": self.seed,
        }

        response = self.llm.invoke(
            prompt
        )

        return self._safe_text(
            response.content
        )

    def generate_with_metadata(
        self,
        mode: str,
        user_query: str,
        query_id: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> Dict[str, Any]:
        """
        Recommended API for the revised run_generation.py.
        """

        response = self.generate_response(
            user_query=user_query,
            query_id=query_id,
            mode_type=mode,
            context_data=context_data,
            use_ood_rule=use_ood_rule,
            use_template=use_template,
        )

        return {
            "response": response,
            "prompt": self.last_prompt,
            "prompt_sha256": (
                self.last_prompt_sha256
            ),
            "prompt_metadata": dict(
                self.last_prompt_metadata
            ),
        }

    def generate(
        self,
        mode: str,
        user_query: str,
        query_id: str,
        context_data: Any = None,
        use_ood_rule: bool = True,
        use_template: bool = True,
    ) -> str:
        """
        Backward-compatible API used by run_generation.py.
        """

        return self.generate_response(
            user_query=user_query,
            query_id=query_id,
            mode_type=mode,
            context_data=context_data,
            use_ood_rule=use_ood_rule,
            use_template=use_template,
        )