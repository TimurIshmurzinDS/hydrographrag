import json
from core.database import HydroDatabase

def run_debug():
    db = HydroDatabase()
    # Ищем всё, что связано с рекой Или напрямую
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?p ?o WHERE {
        ?s rdfs:label|<http://smart-water.org/data/WR_KZ/Post_name> ?name .
        FILTER(CONTAINS(LCASE(STR(?name)), "ile river") || CONTAINS(LCASE(STR(?name)), "или") || CONTAINS(LCASE(STR(?name)), "ili"))
        ?s ?p ?o .
    } LIMIT 30
    """
    results = db.execute_query(query)
    
    print("=== ЧТО РЕАЛЬНО ХРАНИТСЯ В УЗЛЕ РЕКИ ИЛИ ===")
    for res in results:
        prop = res['p'].split('/')[-1].split('#')[-1]
        val = res['o']
        print(f"{prop}  --->  {val}")

if __name__ == "__main__":
    run_debug()