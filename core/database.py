import logging
import os
import uuid
from typing import Any, Dict, List

from dotenv import load_dotenv
from SPARQLWrapper import JSON, POST, SPARQLWrapper


load_dotenv()

logger = logging.getLogger(__name__)


class HydroDatabase:
    """
    Lightweight GraphDB connector used by HydroGraphRAG.

    Responsibilities:
      - execute SPARQL SELECT queries;
      - execute SPARQL UPDATE operations;
      - optionally store query provenance.

    Retrieval and ranking logic intentionally live outside this class.
    """

    def __init__(
        self,
        base_url: str | None = None,
        repository: str | None = None,
    ):
        base_url = (
            base_url
            or os.getenv("GRAPHDB_BASE_URL", "http://127.0.0.1:7200")
        ).rstrip("/")

        repository = (
            repository
            or os.getenv("GRAPHDB_REPO", "waterdb")
        )

        self.endpoint = f"{base_url}/repositories/{repository}"
        self.update_endpoint = f"{self.endpoint}/statements"

        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql_update = SPARQLWrapper(self.update_endpoint)

        logger.info(
            "GraphDB connector initialized: %s",
            self.endpoint,
        )

    def execute_query(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Execute a SPARQL SELECT query and return plain dictionaries.
        """
        if not query or not query.strip():
            return []

        try:
            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(JSON)

            payload = self.sparql.query().convert()
            bindings = payload.get("results", {}).get("bindings", [])

            rows = []

            for binding in bindings:
                row = {
                    key: value.get("value")
                    for key, value in binding.items()
                }
                rows.append(row)

            return rows

        except Exception:
            logger.exception("SPARQL SELECT query failed.")
            return []

    def execute_update(
        self,
        query: str,
    ) -> bool:
        """
        Execute a SPARQL UPDATE statement.
        """
        if not query or not query.strip():
            return False

        try:
            self.sparql_update.setQuery(query)
            self.sparql_update.setMethod(POST)
            self.sparql_update.query()
            return True

        except Exception:
            logger.exception("SPARQL UPDATE failed.")
            return False

    @staticmethod
    def _escape_literal(value: Any) -> str:
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\r", " ")
            .replace("\n", " ")
        )

    def save_solution_graph(
        self,
        query_text: str,
        triples,
        model_name: str,
    ) -> bool:
        """
        Store lightweight provenance linking a user query to graph
        entities used during generation.

        This operation is optional and is not required for retrieval.
        """
        if not triples:
            return False

        node_names = set()

        for triple in triples:
            if not isinstance(triple, dict):
                continue

            source = triple.get("from")
            target = triple.get("to")

            if source and len(str(source)) > 1:
                node_names.add(str(source))

            if target and len(str(target)) > 1:
                node_names.add(str(target))

        if not node_names:
            return False

        query_id = uuid.uuid4().hex

        safe_query = self._escape_literal(query_text)
        safe_model = self._escape_literal(model_name)

        escaped_names = [
            f'"{self._escape_literal(name)}"'
            for name in sorted(node_names)
        ]

        names_filter = ", ".join(escaped_names)

        sparql_update = f"""
        PREFIX log: <http://smart-water.org/log/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wr_kz: <http://smart-water.org/data/WR_KZ/>

        INSERT {{
            <http://smart-water.org/log/Query_{query_id}>
                a log:UserQuery ;
                log:text "{safe_query}" ;
                log:model "{safe_model}" ;
                log:utilizedNode ?target .
        }}
        WHERE {{
            ?target rdfs:label|wr_kz:Post_name ?name .
            FILTER(?name IN ({names_filter}))
        }}
        """

        return self.execute_update(sparql_update)

    def clear_solution_graphs(self) -> bool:
        """
        Remove previously stored UserQuery provenance records.
        """
        query = """
        PREFIX log: <http://smart-water.org/log/>

        DELETE {
            ?query ?predicate ?object
        }
        WHERE {
            ?query a log:UserQuery ;
                   ?predicate ?object .
        }
        """

        return self.execute_update(query)

    def close(self) -> None:
        """
        SPARQLWrapper does not require an explicit connection close.
        Kept for compatibility with the public pipeline API.
        """
        return None
