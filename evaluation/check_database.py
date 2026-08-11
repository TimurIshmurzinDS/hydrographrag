import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


# ============================================================
# CONFIG
# ============================================================

GRAPHDB_URL = "http://localhost:7200"
REPOSITORY_ID = "waterdb"

SPARQL_ENDPOINT = f"{GRAPHDB_URL}/repositories/{REPOSITORY_ID}"

OUTPUT_JSON = "graphdb_audit_report.json"
OUTPUT_TXT = "graphdb_audit_report.txt"

REQUEST_TIMEOUT = 120

TOP_PREDICATES_LIMIT = 100
TOP_CLASSES_LIMIT = 100
TOP_DATATYPES_LIMIT = 100
SAMPLE_LIMIT = 30
WKT_DETAIL_LIMIT = 200

# Optional.
# If ground_truth.json exists next to this script, the audit will also
# inspect how benchmark expected_entities / expected_wkt relate to GraphDB.
GT_PATH = "ground_truth.json"


# ============================================================
# SPARQL CLIENT
# ============================================================

class GraphDBAudit:

    def __init__(self):
        self.endpoint = SPARQL_ENDPOINT
        self.session = requests.Session()

        self.report: Dict[str, Any] = {
            "metadata": {
                "graphdb_url": GRAPHDB_URL,
                "repository_id": REPOSITORY_ID,
                "sparql_endpoint": SPARQL_ENDPOINT,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "python": sys.version,
            },
            "errors": [],
        }

    # --------------------------------------------------------
    # SPARQL
    # --------------------------------------------------------

    def query(self, sparql: str, label: str) -> List[Dict[str, str]]:
        try:
            response = self.session.post(
                self.endpoint,
                data={"query": sparql},
                headers={
                    "Accept": "application/sparql-results+json",
                },
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            data = response.json()

            rows = []

            for binding in data.get("results", {}).get("bindings", []):
                row = {}

                for key, value in binding.items():
                    row[key] = value.get("value", "")

                    datatype = value.get("datatype")
                    language = value.get("xml:lang")

                    if datatype:
                        row[f"{key}__datatype"] = datatype

                    if language:
                        row[f"{key}__lang"] = language

                rows.append(row)

            return rows

        except Exception as exc:
            error = {
                "section": label,
                "error": str(exc),
                "query": sparql,
            }

            self.report["errors"].append(error)

            print(f"❌ {label}: {exc}")

            return []

    # --------------------------------------------------------
    # ASK / scalar helpers
    # --------------------------------------------------------

    def scalar(
        self,
        sparql: str,
        variable: str,
        label: str,
        default: Any = None,
    ) -> Any:
        rows = self.query(
            sparql,
            label,
        )

        if not rows:
            return default

        return rows[0].get(
            variable,
            default,
        )

    @staticmethod
    def local_name(uri: str) -> str:
        text = str(uri or "").strip()

        if "#" in text:
            return text.rsplit("#", 1)[-1]

        if "/" in text:
            return text.rstrip("/").rsplit("/", 1)[-1]

        return text

    # ========================================================
    # CONNECTION
    # ========================================================

    def check_connection(self):
        print("⏳ Проверка подключения к GraphDB...")

        rows = self.query(
            """
            SELECT ?s
            WHERE {
                ?s ?p ?o .
            }
            LIMIT 1
            """,
            "connection_test",
        )

        connected = bool(rows)

        self.report["metadata"]["connection_ok"] = connected

        if connected:
            print(f"✅ GraphDB доступен: {self.endpoint}")
        else:
            raise RuntimeError(
                "Не удалось прочитать ни одного triple из GraphDB."
            )

    # ========================================================
    # GLOBAL STATISTICS
    # ========================================================

    def collect_global_statistics(self):
        print("📊 1. Общая статистика...")

        total_triples = self.scalar(
            """
            SELECT (COUNT(*) AS ?count)
            WHERE {
                ?s ?p ?o .
            }
            """,
            "count",
            "total_triples",
            "0",
        )

        unique_subjects = self.scalar(
            """
            SELECT (COUNT(DISTINCT ?s) AS ?count)
            WHERE {
                ?s ?p ?o .
            }
            """,
            "count",
            "unique_subjects",
            "0",
        )

        unique_predicates = self.scalar(
            """
            SELECT (COUNT(DISTINCT ?p) AS ?count)
            WHERE {
                ?s ?p ?o .
            }
            """,
            "count",
            "unique_predicates",
            "0",
        )

        unique_objects = self.scalar(
            """
            SELECT (COUNT(DISTINCT ?o) AS ?count)
            WHERE {
                ?s ?p ?o .
            }
            """,
            "count",
            "unique_objects",
            "0",
        )

        literal_objects = self.scalar(
            """
            SELECT (COUNT(*) AS ?count)
            WHERE {
                ?s ?p ?o .
                FILTER(isLiteral(?o))
            }
            """,
            "count",
            "literal_objects",
            "0",
        )

        iri_objects = self.scalar(
            """
            SELECT (COUNT(*) AS ?count)
            WHERE {
                ?s ?p ?o .
                FILTER(isIRI(?o))
            }
            """,
            "count",
            "iri_objects",
            "0",
        )

        blank_nodes = self.scalar(
            """
            SELECT (COUNT(DISTINCT ?x) AS ?count)
            WHERE {
                {
                    ?x ?p ?o .
                    FILTER(isBlank(?x))
                }
                UNION
                {
                    ?s ?p ?x .
                    FILTER(isBlank(?x))
                }
            }
            """,
            "count",
            "blank_nodes",
            "0",
        )

        self.report["global_statistics"] = {
            "total_triples": int(total_triples or 0),
            "unique_subjects": int(unique_subjects or 0),
            "unique_predicates": int(unique_predicates or 0),
            "unique_objects": int(unique_objects or 0),
            "literal_object_triples": int(literal_objects or 0),
            "iri_object_triples": int(iri_objects or 0),
            "unique_blank_nodes": int(blank_nodes or 0),
        }

    # ========================================================
    # CLASSES
    # ========================================================

    def collect_classes(self):
        print("🏷️ 2. Классы...")

        rows = self.query(
            f"""
            SELECT ?class (COUNT(DISTINCT ?s) AS ?count)
            WHERE {{
                ?s a ?class .
            }}
            GROUP BY ?class
            ORDER BY DESC(?count)
            LIMIT {TOP_CLASSES_LIMIT}
            """,
            "classes",
        )

        result = []

        for row in rows:
            result.append({
                "class_uri": row.get("class", ""),
                "class_local": self.local_name(
                    row.get("class", "")
                ),
                "count": int(row.get("count", 0)),
            })

        self.report["classes"] = result

    # ========================================================
    # PREDICATES
    # ========================================================

    def collect_predicates(self):
        print("🔗 3. Предикаты...")

        rows = self.query(
            f"""
            SELECT ?p
                   (COUNT(*) AS ?count)
                   (COUNT(DISTINCT ?s) AS ?subjects)
                   (COUNT(DISTINCT ?o) AS ?objects)
            WHERE {{
                ?s ?p ?o .
            }}
            GROUP BY ?p
            ORDER BY DESC(?count)
            LIMIT {TOP_PREDICATES_LIMIT}
            """,
            "predicates",
        )

        predicates = []

        for row in rows:
            predicate_uri = row.get("p", "")

            predicate_stats = self.query(
                f"""
                SELECT
                    (SUM(IF(isLiteral(?o), 1, 0)) AS ?literal_count)
                    (SUM(IF(isIRI(?o), 1, 0)) AS ?iri_count)
                    (SUM(IF(isBlank(?o), 1, 0)) AS ?blank_count)
                WHERE {{
                    ?s <{predicate_uri}> ?o .
                }}
                """,
                f"predicate_object_type:{predicate_uri}",
            )

            stat = (
                predicate_stats[0]
                if predicate_stats
                else {}
            )

            predicates.append({
                "predicate_uri": predicate_uri,
                "predicate_local": self.local_name(predicate_uri),
                "count": int(row.get("count", 0)),
                "distinct_subjects": int(row.get("subjects", 0)),
                "distinct_objects": int(row.get("objects", 0)),
                "literal_object_count": int(
                    stat.get("literal_count", 0) or 0
                ),
                "iri_object_count": int(
                    stat.get("iri_count", 0) or 0
                ),
                "blank_object_count": int(
                    stat.get("blank_count", 0) or 0
                ),
            })

        self.report["predicates"] = predicates

    # ========================================================
    # LITERAL DATATYPES
    # ========================================================

    def collect_literal_datatypes(self):
        print("🔢 4. Типы literals...")

        rows = self.query(
            f"""
            SELECT ?datatype (COUNT(*) AS ?count)
            WHERE {{
                ?s ?p ?o .
                FILTER(isLiteral(?o))
                BIND(DATATYPE(?o) AS ?datatype)
            }}
            GROUP BY ?datatype
            ORDER BY DESC(?count)
            LIMIT {TOP_DATATYPES_LIMIT}
            """,
            "literal_datatypes",
        )

        self.report["literal_datatypes"] = [
            {
                "datatype": row.get("datatype", ""),
                "datatype_local": self.local_name(
                    row.get("datatype", "")
                ),
                "count": int(row.get("count", 0)),
            }
            for row in rows
        ]

    # ========================================================
    # LABEL PREDICATES
    # ========================================================

    def collect_label_predicates(self):
        print("🏷️ 5. Потенциальные label/name predicates...")

        rows = self.query(
            """
            SELECT ?p (COUNT(*) AS ?count)
            WHERE {
                ?s ?p ?o .
                FILTER(isLiteral(?o))

                FILTER(
                    CONTAINS(LCASE(STR(?p)), "label")
                    ||
                    CONTAINS(LCASE(STR(?p)), "name")
                )
            }
            GROUP BY ?p
            ORDER BY DESC(?count)
            """,
            "label_predicates",
        )

        result = []

        for row in rows:
            result.append({
                "predicate_uri": row.get("p", ""),
                "predicate_local": self.local_name(
                    row.get("p", "")
                ),
                "count": int(row.get("count", 0)),
            })

        self.report["label_predicates"] = result

    # ========================================================
    # WKT
    # ========================================================

    def collect_wkt(self):
        print("🗺️ 6. WKT структура...")

        wkt_predicates = self.query(
            """
            SELECT ?p (COUNT(*) AS ?count)
            WHERE {
                ?s ?p ?o .

                FILTER(
                    CONTAINS(
                        LCASE(STR(?p)),
                        "wkt"
                    )
                )
            }
            GROUP BY ?p
            ORDER BY DESC(?count)
            """,
            "wkt_predicates",
        )

        self.report["wkt_predicates"] = [
            {
                "predicate_uri": row.get("p", ""),
                "predicate_local": self.local_name(
                    row.get("p", "")
                ),
                "count": int(row.get("count", 0)),
            }
            for row in wkt_predicates
        ]

        wkt_rows = self.query(
            f"""
            SELECT ?s ?p ?wkt
            WHERE {{
                ?s ?p ?wkt .

                FILTER(
                    CONTAINS(
                        LCASE(STR(?p)),
                        "wkt"
                    )
                )
            }}
            ORDER BY ?s
            LIMIT {WKT_DETAIL_LIMIT}
            """,
            "wkt_values",
        )

        wkt_details = []

        for row in wkt_rows:
            subject = row.get("s", "")

            neighbors = self.query(
                """
                SELECT ?p ?o
                WHERE {
                    <%s> ?p ?o .
                }
                ORDER BY ?p
                LIMIT 50
                """ % subject,
                f"wkt_neighbors:{subject}",
            )

            incoming = self.query(
                """
                SELECT ?s ?p
                WHERE {
                    ?s ?p <%s> .
                }
                ORDER BY ?p
                LIMIT 50
                """ % subject,
                f"wkt_incoming:{subject}",
            )

            wkt_details.append({
                "subject": subject,
                "subject_local": self.local_name(subject),
                "predicate": row.get("p", ""),
                "predicate_local": self.local_name(
                    row.get("p", "")
                ),
                "wkt": row.get("wkt", ""),
                "wkt_datatype": row.get(
                    "wkt__datatype",
                    "",
                ),
                "outgoing_neighbors": neighbors,
                "incoming_neighbors": incoming,
            })

        self.report["wkt_details"] = wkt_details

    # ========================================================
    # HYDRO FEATURES
    # ========================================================

    def collect_hydro_features(self):
        print("🌊 7. Hydro features...")

        rows = self.query(
            f"""
            SELECT DISTINCT ?s ?class
            WHERE {{
                ?s a ?class .

                FILTER(
                    CONTAINS(
                        LCASE(STR(?class)),
                        "hydrofeature"
                    )
                    ||
                    CONTAINS(
                        LCASE(STR(?class)),
                        "river"
                    )
                    ||
                    CONTAINS(
                        LCASE(STR(?class)),
                        "waterbody"
                    )
                )
            }}
            ORDER BY ?s
            LIMIT {SAMPLE_LIMIT}
            """,
            "hydro_features",
        )

        features = []

        for row in rows:
            subject = row.get("s", "")

            outgoing = self.query(
                """
                SELECT ?p ?o
                WHERE {
                    <%s> ?p ?o .
                }
                ORDER BY ?p
                LIMIT 100
                """ % subject,
                f"hydro_feature_outgoing:{subject}",
            )

            incoming = self.query(
                """
                SELECT ?s ?p
                WHERE {
                    ?s ?p <%s> .
                }
                ORDER BY ?p
                LIMIT 100
                """ % subject,
                f"hydro_feature_incoming:{subject}",
            )

            features.append({
                "subject": subject,
                "subject_local": self.local_name(subject),
                "class": row.get("class", ""),
                "class_local": self.local_name(
                    row.get("class", "")
                ),
                "outgoing": outgoing,
                "incoming": incoming,
            })

        self.report["hydro_feature_samples"] = features

    # ========================================================
    # OBSERVATION STRUCTURE
    # ========================================================

    def collect_observation_structure(self):
        print("📡 8. Observation structure...")

        observation_classes = self.query(
            """
            SELECT ?class (COUNT(DISTINCT ?s) AS ?count)
            WHERE {
                ?s a ?class .

                FILTER(
                    CONTAINS(
                        LCASE(STR(?class)),
                        "observation"
                    )
                )
            }
            GROUP BY ?class
            ORDER BY DESC(?count)
            """,
            "observation_classes",
        )

        self.report["observation_classes"] = [
            {
                "class": row.get("class", ""),
                "class_local": self.local_name(
                    row.get("class", "")
                ),
                "count": int(row.get("count", 0)),
            }
            for row in observation_classes
        ]

        if not observation_classes:
            self.report["observation_predicates"] = []
            self.report["observation_samples"] = []
            return

        # Use every detected observation class.
        class_values = " ".join(
            f"<{row['class']}>"
            for row in observation_classes
            if row.get("class")
        )

        predicate_rows = self.query(
            f"""
            SELECT ?p (COUNT(*) AS ?count)
            WHERE {{
                ?obs a ?class .
                VALUES ?class {{ {class_values} }}
                ?obs ?p ?o .
            }}
            GROUP BY ?p
            ORDER BY DESC(?count)
            """,
            "observation_predicates",
        )

        self.report["observation_predicates"] = [
            {
                "predicate_uri": row.get("p", ""),
                "predicate_local": self.local_name(
                    row.get("p", "")
                ),
                "count": int(row.get("count", 0)),
            }
            for row in predicate_rows
        ]

        samples = self.query(
            f"""
            SELECT DISTINCT ?obs
            WHERE {{
                ?obs a ?class .
                VALUES ?class {{ {class_values} }}
            }}
            ORDER BY ?obs
            LIMIT {SAMPLE_LIMIT}
            """,
            "observation_samples",
        )

        observation_samples = []

        for row in samples:
            obs = row.get("obs", "")

            outgoing = self.query(
                """
                SELECT ?p ?o
                WHERE {
                    <%s> ?p ?o .
                }
                ORDER BY ?p
                LIMIT 100
                """ % obs,
                f"observation_outgoing:{obs}",
            )

            incoming = self.query(
                """
                SELECT ?s ?p
                WHERE {
                    ?s ?p <%s> .
                }
                ORDER BY ?p
                LIMIT 100
                """ % obs,
                f"observation_incoming:{obs}",
            )

            observation_samples.append({
                "observation": obs,
                "observation_local": self.local_name(obs),
                "outgoing": outgoing,
                "incoming": incoming,
            })

        self.report["observation_samples"] = observation_samples

    # ========================================================
    # IMPORTANT HYDROLOGICAL PREDICATES
    # ========================================================

    def collect_hydrological_predicates(self):
        print("💧 9. Гидрологические literals и temporal predicates...")

        keywords = [
            "water_level",
            "waterlevel",
            "water_consumption",
            "discharge",
            "flow",
            "volume",
            "width",
            "length",
            "time",
            "date",
            "concentration",
            "quality",
            "basin",
            "region",
            "featureofinterest",
            "result",
            "location",
        ]

        filters = "\n||\n".join(
            f'CONTAINS(LCASE(STR(?p)), "{keyword}")'
            for keyword in keywords
        )

        rows = self.query(
            f"""
            SELECT ?p
                   (COUNT(*) AS ?count)
                   (COUNT(DISTINCT ?s) AS ?subjects)
                   (COUNT(DISTINCT ?o) AS ?objects)
            WHERE {{
                ?s ?p ?o .

                FILTER(
                    {filters}
                )
            }}
            GROUP BY ?p
            ORDER BY DESC(?count)
            """,
            "hydrological_predicates",
        )

        details = []

        for row in rows:
            predicate = row.get("p", "")

            samples = self.query(
                """
                SELECT ?s ?o
                WHERE {
                    ?s <%s> ?o .
                }
                LIMIT 10
                """ % predicate,
                f"predicate_samples:{predicate}",
            )

            details.append({
                "predicate_uri": predicate,
                "predicate_local": self.local_name(predicate),
                "count": int(row.get("count", 0)),
                "distinct_subjects": int(row.get("subjects", 0)),
                "distinct_objects": int(row.get("objects", 0)),
                "samples": samples,
            })

        self.report["hydrological_predicates"] = details

    # ========================================================
    # PROPERTY / SUBPROPERTY STRUCTURE
    # ========================================================

    def collect_property_hierarchy(self):
        print("🧩 10. Property hierarchy...")

        rows = self.query(
            """
            SELECT ?child ?parent
            WHERE {
                ?child
                    <http://www.w3.org/2000/01/rdf-schema#subPropertyOf>
                    ?parent .
            }
            ORDER BY ?child
            """,
            "subproperties",
        )

        self.report["subproperties"] = [
            {
                "child": row.get("child", ""),
                "child_local": self.local_name(
                    row.get("child", "")
                ),
                "parent": row.get("parent", ""),
                "parent_local": self.local_name(
                    row.get("parent", "")
                ),
            }
            for row in rows
        ]

    # ========================================================
    # PREDICATE PAIRS / LOCAL TOPOLOGY
    # ========================================================

    def collect_common_two_hop_patterns(self):
        print("🕸️ 11. Частые двухшаговые пути...")

        rows = self.query(
            """
            SELECT ?p1 ?p2 (COUNT(*) AS ?count)
            WHERE {
                ?a ?p1 ?b .
                FILTER(isIRI(?b))
                ?b ?p2 ?c .
            }
            GROUP BY ?p1 ?p2
            ORDER BY DESC(?count)
            LIMIT 100
            """,
            "two_hop_patterns",
        )

        self.report["two_hop_patterns"] = [
            {
                "p1": row.get("p1", ""),
                "p1_local": self.local_name(
                    row.get("p1", "")
                ),
                "p2": row.get("p2", ""),
                "p2_local": self.local_name(
                    row.get("p2", "")
                ),
                "count": int(row.get("count", 0)),
            }
            for row in rows
        ]

    # ========================================================
    # URI NAMESPACES
    # ========================================================

    def collect_namespaces(self):
        print("🌐 12. URI namespaces...")

        rows = self.query(
            """
            SELECT DISTINCT ?x
            WHERE {
                {
                    ?x ?p ?o .
                    FILTER(isIRI(?x))
                }
                UNION
                {
                    ?s ?x ?o .
                    FILTER(isIRI(?x))
                }
                UNION
                {
                    ?s ?p ?x .
                    FILTER(isIRI(?x))
                }
            }
            LIMIT 200000
            """,
            "uri_namespace_scan",
        )

        namespace_counter = Counter()

        for row in rows:
            uri = row.get("x", "")

            if "#" in uri:
                namespace = uri.rsplit("#", 1)[0] + "#"
            elif "/" in uri:
                namespace = uri.rsplit("/", 1)[0] + "/"
            else:
                namespace = uri

            namespace_counter[namespace] += 1

        self.report["uri_namespaces"] = [
            {
                "namespace": namespace,
                "count": count,
            }
            for namespace, count
            in namespace_counter.most_common(100)
        ]

    # ========================================================
    # BENCHMARK CROSS-CHECK
    # ========================================================

    def collect_benchmark_crosscheck(self):
        print("🧪 13. Сверка с ground_truth.json...")

        if not os.path.isfile(GT_PATH):
            self.report["benchmark_crosscheck"] = {
                "available": False,
                "reason": (
                    f"{GT_PATH} not found next to script."
                ),
            }

            print(
                "⚠️ ground_truth.json не найден рядом со скриптом; "
                "benchmark cross-check пропущен."
            )
            return

        try:
            with open(
                GT_PATH,
                "r",
                encoding="utf-8",
            ) as f:
                gt = json.load(f)

        except Exception as exc:
            self.report["benchmark_crosscheck"] = {
                "available": False,
                "reason": str(exc),
            }
            return

        expected_entities = []
        expected_wkts = []

        for item in gt:
            if not isinstance(item, dict):
                continue

            for entity in item.get(
                "expected_entities",
                [],
            ):
                if entity:
                    expected_entities.append(str(entity))

            for geometry in item.get(
                "expected_wkt",
                [],
            ):
                if geometry:
                    expected_wkts.append(str(geometry))

        unique_entities = sorted(set(expected_entities))
        unique_wkts = sorted(set(expected_wkts))

        # Pull likely labels/names once, then compare locally.
        label_rows = self.query(
            """
            SELECT ?s ?p ?label
            WHERE {
                ?s ?p ?label .
                FILTER(isLiteral(?label))
                FILTER(
                    CONTAINS(LCASE(STR(?p)), "label")
                    ||
                    CONTAINS(LCASE(STR(?p)), "name")
                )
            }
            """,
            "benchmark_labels",
        )

        graph_labels = defaultdict(list)

        for row in label_rows:
            label = row.get("label", "").strip().lower()

            if label:
                graph_labels[label].append({
                    "subject": row.get("s", ""),
                    "predicate": row.get("p", ""),
                    "label": row.get("label", ""),
                })

        entity_matches = []

        for entity in unique_entities:
            key = entity.strip().lower()

            exact = graph_labels.get(
                key,
                [],
            )

            entity_matches.append({
                "expected_entity": entity,
                "exact_label_match_count": len(exact),
                "exact_matches": exact[:20],
            })

        graph_wkt_rows = self.query(
            """
            SELECT ?s ?p ?wkt
            WHERE {
                ?s ?p ?wkt .
                FILTER(
                    CONTAINS(
                        LCASE(STR(?p)),
                        "wkt"
                    )
                )
            }
            """,
            "benchmark_wkt_values",
        )

        graph_wkt_lookup = defaultdict(list)

        for row in graph_wkt_rows:
            value = row.get("wkt", "").strip()

            if value:
                graph_wkt_lookup[value].append({
                    "subject": row.get("s", ""),
                    "predicate": row.get("p", ""),
                })

        wkt_matches = []

        for expected in unique_wkts:
            exact = graph_wkt_lookup.get(
                expected,
                [],
            )

            wkt_matches.append({
                "expected_wkt": expected,
                "exact_match_count": len(exact),
                "matches": exact[:20],
            })

        self.report["benchmark_crosscheck"] = {
            "available": True,
            "benchmark_items": len(gt),
            "unique_expected_entities": len(unique_entities),
            "unique_expected_wkt": len(unique_wkts),
            "entities_with_exact_label_match": sum(
                1
                for item in entity_matches
                if item["exact_label_match_count"] > 0
            ),
            "wkt_with_exact_match": sum(
                1
                for item in wkt_matches
                if item["exact_match_count"] > 0
            ),
            "entity_matches": entity_matches,
            "wkt_matches": wkt_matches,
        }

    # ========================================================
    # REPORT SUMMARY
    # ========================================================

    def build_summary(self):
        print("📝 14. Формирование summary...")

        global_stats = self.report.get(
            "global_statistics",
            {},
        )

        classes = self.report.get(
            "classes",
            [],
        )

        predicates = self.report.get(
            "predicates",
            [],
        )

        wkt_details = self.report.get(
            "wkt_details",
            [],
        )

        obs_classes = self.report.get(
            "observation_classes",
            [],
        )

        benchmark = self.report.get(
            "benchmark_crosscheck",
            {},
        )

        self.report["summary"] = {
            "total_triples": global_stats.get(
                "total_triples",
                0,
            ),
            "top_classes": [
                {
                    "class": item["class_local"],
                    "count": item["count"],
                }
                for item in classes[:20]
            ],
            "top_predicates": [
                {
                    "predicate": item["predicate_local"],
                    "count": item["count"],
                    "literal_objects": item[
                        "literal_object_count"
                    ],
                    "iri_objects": item[
                        "iri_object_count"
                    ],
                }
                for item in predicates[:30]
            ],
            "wkt_count_in_audit": len(wkt_details),
            "observation_classes": obs_classes,
            "benchmark_crosscheck_available": benchmark.get(
                "available",
                False,
            ),
            "benchmark_entities_exact_match": benchmark.get(
                "entities_with_exact_label_match",
            ),
            "benchmark_unique_expected_entities": benchmark.get(
                "unique_expected_entities",
            ),
            "benchmark_wkt_exact_match": benchmark.get(
                "wkt_with_exact_match",
            ),
            "benchmark_unique_expected_wkt": benchmark.get(
                "unique_expected_wkt",
            ),
            "error_count": len(
                self.report.get(
                    "errors",
                    [],
                )
            ),
        }

    # ========================================================
    # TXT REPORT
    # ========================================================

    def save_txt_report(self):
        lines = []

        lines.append("=" * 80)
        lines.append("GRAPHDB AUDIT REPORT")
        lines.append("=" * 80)
        lines.append("")

        metadata = self.report.get("metadata", {})

        lines.append(
            f"Repository: {metadata.get('repository_id')}"
        )
        lines.append(
            f"Endpoint: {metadata.get('sparql_endpoint')}"
        )
        lines.append(
            f"Created: {metadata.get('created_at')}"
        )
        lines.append("")

        summary = self.report.get("summary", {})

        lines.append("-" * 80)
        lines.append("SUMMARY")
        lines.append("-" * 80)

        for key, value in summary.items():
            if key in {
                "top_classes",
                "top_predicates",
                "observation_classes",
            }:
                continue

            lines.append(
                f"{key}: {value}"
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("TOP CLASSES")
        lines.append("-" * 80)

        for item in summary.get("top_classes", []):
            lines.append(
                f"{item['class']}: {item['count']}"
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("TOP PREDICATES")
        lines.append("-" * 80)

        for item in summary.get("top_predicates", []):
            lines.append(
                (
                    f"{item['predicate']}: {item['count']} "
                    f"(literal={item['literal_objects']}, "
                    f"iri={item['iri_objects']})"
                )
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("WKT PREDICATES")
        lines.append("-" * 80)

        for item in self.report.get(
            "wkt_predicates",
            [],
        ):
            lines.append(
                (
                    f"{item['predicate_local']} "
                    f"[{item['predicate_uri']}]: "
                    f"{item['count']}"
                )
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("LABEL PREDICATES")
        lines.append("-" * 80)

        for item in self.report.get(
            "label_predicates",
            [],
        ):
            lines.append(
                (
                    f"{item['predicate_local']} "
                    f"[{item['predicate_uri']}]: "
                    f"{item['count']}"
                )
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("OBSERVATION PREDICATES")
        lines.append("-" * 80)

        for item in self.report.get(
            "observation_predicates",
            [],
        ):
            lines.append(
                (
                    f"{item['predicate_local']}: "
                    f"{item['count']}"
                )
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("IMPORTANT HYDROLOGICAL PREDICATES")
        lines.append("-" * 80)

        for item in self.report.get(
            "hydrological_predicates",
            [],
        ):
            lines.append(
                (
                    f"{item['predicate_local']}: "
                    f"{item['count']} "
                    f"(subjects={item['distinct_subjects']}, "
                    f"objects={item['distinct_objects']})"
                )
            )

            for sample in item.get("samples", [])[:3]:
                lines.append(
                    (
                        f"    {self.local_name(sample.get('s', ''))} "
                        f"-> {sample.get('o', '')}"
                    )
                )

        lines.append("")
        lines.append("-" * 80)
        lines.append("COMMON 2-HOP PATTERNS")
        lines.append("-" * 80)

        for item in self.report.get(
            "two_hop_patterns",
            [],
        )[:50]:
            lines.append(
                (
                    f"{item['p1_local']} -> "
                    f"{item['p2_local']}: "
                    f"{item['count']}"
                )
            )

        benchmark = self.report.get(
            "benchmark_crosscheck",
            {},
        )

        lines.append("")
        lines.append("-" * 80)
        lines.append("BENCHMARK CROSS-CHECK")
        lines.append("-" * 80)

        if benchmark.get("available"):
            lines.append(
                (
                    "Expected entities with exact label match: "
                    f"{benchmark.get('entities_with_exact_label_match')} / "
                    f"{benchmark.get('unique_expected_entities')}"
                )
            )

            lines.append(
                (
                    "Expected WKT with exact DB match: "
                    f"{benchmark.get('wkt_with_exact_match')} / "
                    f"{benchmark.get('unique_expected_wkt')}"
                )
            )

            missing_entities = [
                item["expected_entity"]
                for item in benchmark.get(
                    "entity_matches",
                    [],
                )
                if item.get(
                    "exact_label_match_count",
                    0,
                ) == 0
            ]

            lines.append("")
            lines.append(
                "Expected entities without exact label match:"
            )

            for entity in missing_entities:
                lines.append(
                    f"    - {entity}"
                )

            missing_wkt = [
                item["expected_wkt"]
                for item in benchmark.get(
                    "wkt_matches",
                    [],
                )
                if item.get(
                    "exact_match_count",
                    0,
                ) == 0
            ]

            lines.append("")
            lines.append(
                "Expected WKT without exact DB match:"
            )

            for geometry in missing_wkt:
                lines.append(
                    f"    - {geometry}"
                )

        else:
            lines.append(
                "ground_truth.json was not available."
            )

        lines.append("")
        lines.append("-" * 80)
        lines.append("ERRORS")
        lines.append("-" * 80)

        errors = self.report.get(
            "errors",
            [],
        )

        if errors:
            for error in errors:
                lines.append(
                    (
                        f"{error.get('section')}: "
                        f"{error.get('error')}"
                    )
                )
        else:
            lines.append("No SPARQL errors.")

        with open(
            OUTPUT_TXT,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                "\n".join(lines)
            )

    # ========================================================
    # RUN
    # ========================================================

    def run(self):
        started = time.perf_counter()

        self.check_connection()

        self.collect_global_statistics()
        self.collect_classes()
        self.collect_predicates()
        self.collect_literal_datatypes()
        self.collect_label_predicates()
        self.collect_wkt()
        self.collect_hydro_features()
        self.collect_observation_structure()
        self.collect_hydrological_predicates()
        self.collect_property_hierarchy()
        self.collect_common_two_hop_patterns()
        self.collect_namespaces()
        self.collect_benchmark_crosscheck()

        self.build_summary()

        self.report[
            "metadata"
        ][
            "audit_duration_seconds"
        ] = round(
            time.perf_counter() - started,
            3,
        )

        with open(
            OUTPUT_JSON,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                self.report,
                f,
                ensure_ascii=False,
                indent=2,
            )

        self.save_txt_report()

        print("")
        print("=" * 70)
        print("✅ АУДИТ ЗАВЕРШЁН")
        print("=" * 70)
        print(f"📄 JSON: {os.path.abspath(OUTPUT_JSON)}")
        print(f"📄 TXT : {os.path.abspath(OUTPUT_TXT)}")
        print(
            "⚠️ Если JSON большой — пришли мне именно JSON. "
            "TXT можно приложить дополнительно."
        )


if __name__ == "__main__":
    GraphDBAudit().run()