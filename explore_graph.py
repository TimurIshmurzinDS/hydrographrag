from core.database import HydroDatabase

def explore():
    print("⏳ Подключение к GraphDB для анализа структуры...")
    db = HydroDatabase()
    
    print("\n📊 1. СТАТИСТИКА КЛАССОВ (Категории узлов):")
    query_cats = """
    SELECT ?category (COUNT(?s) AS ?count) WHERE {
        ?s a ?type .
        BIND(REPLACE(STR(?type), "^.*[#/](.+)$", "$1") AS ?category)
    } GROUP BY ?category ORDER BY DESC(?count)
    """
    cats = db.execute_query(query_cats)
    for c in cats:
        print(f" 🏷️ {c['category']}: {c['count']} узлов")

    print("\n🗂 2. СТАТИСТИКА СВЯЗЕЙ (Предикаты):")
    query_rels = """
    SELECT ?relation (COUNT(?p) AS ?count) WHERE {
        ?s ?p ?o .
        BIND(REPLACE(STR(?p), "^.*[#/](.+)$", "$1") AS ?relation)
        FILTER(?relation != "type")
    } GROUP BY ?relation ORDER BY DESC(?count)
    """
    rels = db.execute_query(query_rels)
    for r in rels:
        print(f" 🔗 {r['relation']}: {r['count']} связей")

    print("\n🔍 3. ПРИМЕР СВЯЗЕЙ В БАЗЕ (Реки и Регионы):")
    query_examples = """
    PREFIX hyf: <http://www.opengis.net/ont/hy_features#>
    PREFIX sw: <http://smart-water.org/data/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sg_kz: <http://smart-water.org/data/SocioGeo_KZ/>

    SELECT ?riverName ?regionName WHERE {
        ?river a hyf:HY_HydroFeature ;
               sw:locatedInRegion ?region .
        
        OPTIONAL { ?river rdfs:label ?r_lbl }
        OPTIONAL { ?region rdfs:label ?reg_lbl }
        
        BIND(COALESCE(?r_lbl, REPLACE(STR(?river), "^.*[#/](.+)$", "$1")) AS ?riverName)
        BIND(COALESCE(?reg_lbl, REPLACE(STR(?region), "^.*[#/](.+)$", "$1")) AS ?regionName)
    } LIMIT 10
    """
    examples = db.execute_query(query_examples)
    if examples:
        for ex in examples:
            print(f"🌊 {ex.get('riverName')} -> [locatedInRegion] -> 🗺️ {ex.get('regionName')}")
    else:
        print("Связи 'locatedInRegion' не найдены или запрос требует корректировки.")

if __name__ == "__main__":
    explore()