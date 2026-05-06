from SPARQLWrapper import SPARQLWrapper, JSON

def fetch_wkt_data():
    endpoint = "http://localhost:7200/repositories/waterdb"
    sparql = SPARQLWrapper(endpoint)
    
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wr_kz: <http://smart-water.org/data/WR_KZ/>
    
    SELECT ?name ?wkt WHERE {
        ?entity ?p ?wkt .
        FILTER(CONTAINS(STR(?p), "asWKT"))
        
        OPTIONAL { ?entity rdfs:label ?lbl . }
        OPTIONAL { ?entity wr_kz:Post_name ?post . }
        BIND(COALESCE(?lbl, ?post, REPLACE(STR(?entity), "^.*[#/](.+)$", "$1")) AS ?name)
    } LIMIT 100
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]
        print(f"✅ Найдено объектов с WKT: {len(bindings)}")
        
        for res in bindings:
            name = res["name"]["value"]
            wkt = res["wkt"]["value"]
            print(f"🔹 {name} -> {wkt}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fetch_wkt_data()