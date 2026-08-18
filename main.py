import os
import uuid

from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from planner.generator import SolutionPlanner


MODEL_NAME = os.getenv(
    "HYDROGRAPHRAG_MODEL",
    "qwen2.5-coder:7b",
)


def main() -> None:
    print("\nHydroGraphRAG initialization...")

    db = HydroDatabase()
    embedder = EmbeddingsManager()

    identifier = DemandIdentifier(
        model_name=MODEL_NAME
    )

    retriever = GraphRetriever(
        db,
        embedder,
        model_name=MODEL_NAME,
        reproduce_frozen_nav_bug=False,
    )

    planner = SolutionPlanner(
        model_name=MODEL_NAME,
        num_ctx=8192,
        temperature=0.0,
        top_p=1.0,
        seed=42,
        num_predict=4096,
    )

    print("\nHydroGraphRAG is ready.")
    print(f"Model: {MODEL_NAME}")

    try:
        query = input(
            "\nEnter a hydrology/GIS query: "
        ).strip()

        if not query:
            print("Empty query.")
            return

        query_id = uuid.uuid4().hex[:12]

        # ----------------------------------------------------
        # Context/Demand Analysis
        # ----------------------------------------------------
        demand = identifier.analyze_query(
            query
        )

        category = str(
            demand.get(
                "category",
                "unknown",
            )
        )

        print(
            f"\nCategory: {category}"
        )

        # ----------------------------------------------------
        # OOD
        # ----------------------------------------------------
        if category == "anomalous":
            result = planner.generate_response(
                user_query=query,
                query_id=query_id,
                mode_type="hydrographrag",
                context_data=[],
                use_ood_rule=True,
                use_template=True,
            )

            print("\nResult:\n")
            print(result)
            return

        # ----------------------------------------------------
        # Ontology-grounded retrieval
        # ----------------------------------------------------
        triples = retriever.find_solution_subgraph(
            demand
        )

        print(
            f"Retrieved triples: {len(triples)}"
        )

        # ----------------------------------------------------
        # Generation
        # ----------------------------------------------------
        result = planner.generate_response(
            user_query=query,
            query_id=query_id,
            mode_type="hydrographrag",
            context_data=triples,
            use_ood_rule=True,
            use_template=True,
        )

        # Optional provenance storage.
        if triples:
            db.save_solution_graph(
                query,
                triples,
                MODEL_NAME,
            )

        print("\nResult:\n")
        print(result)

    finally:
        db.close()


if __name__ == "__main__":
    main()
