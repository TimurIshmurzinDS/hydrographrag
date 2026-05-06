import logging

class GraphRetriever:
    """
    Модуль извлечения подграфа GeoGraphRAG.
    Адаптирован под семантические графы знаний RDF (SPARQL).
    Включает семантическое гео-расширение (Geo-Spatial Expansion) для поиска WKT.
    """
    def __init__(self, db_connector, embedder, model_name="qwen2.5-coder:7b"):
        self.db = db_connector
        self.embedder = embedder
        self.logger = logging.getLogger(__name__)
        # Инициализируем модель ОДИН раз при создании класса
        from langchain_ollama import ChatOllama
        self.nav_llm = ChatOllama(model=model_name, temperature=0) 
        
        
        # Префиксы из онтологии, включая geo: для геометрии
        self.prefixes = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wr_kz: <http://smart-water.org/data/WR_KZ/>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX hyf: <http://www.opengis.net/ont/hy_features#>
        PREFIX sg_kz: <http://smart-water.org/data/SocioGeo_KZ/>
        PREFIX sw: <http://smart-water.org/data/>
        PREFIX socio_kz: <http://smart-water.org/ont/socio_kz#>
        PREFIX time: <http://smart-water.org/ont/time#>
        PREFIX unit: <http://smart-water.org/ont/unit#>
        PREFIX vg: <http://waterontology.org/vg#>
        PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        """
    def iterative_navigation(self, query, start_node_id, start_node_name, max_steps=3):
        """
        Интеллектуальный поиск пути (как в статье). 
        LLM сама выбирает, какие узлы в графе ей нужны.
        """
        current_node_id = start_node_id
        current_node_name = start_node_name
        path_triples = []
        visited = {current_node_id}

        print(f"🚀 Начало навигации из узла: {current_node_name}")

        for step in range(max_steps):
            # 1. Получаем список всех соседей текущего узла через SPARQL
            neighbors_query = self.prefixes + f"""
            SELECT ?rel ?neighbor ?nName ?nType WHERE {{
                <{current_node_id}> ?relUri ?neighbor .
                ?neighbor a ?typeUri .
                OPTIONAL {{ ?neighbor wr_kz:Post_name|rdfs:label ?label }}
                BIND(COALESCE(?label, REPLACE(STR(?neighbor), "^.*[#/](.+)$", "$1")) AS ?nName)
                BIND(REPLACE(STR(?relUri), "^.*[#/](.+)$", "$1") AS ?rel)
                BIND(REPLACE(STR(?typeUri), "^.*[#/](.+)$", "$1") AS ?nType)
                FILTER(?rel NOT IN ("type", "hasInstance", "hasAnchor"))
            }} LIMIT 10
            """
            neighbors = self.db.execute_query(neighbors_query)
            if not neighbors: break

            # 2. Формируем список опций для LLM
            options = []
            for i, n in enumerate(neighbors):
                options.append(f"{i}. Узел: '{n['nName']}' (Тип: {n['nType']}) через связь '{n['rel']}'")

            # 3. Просим LLM выбрать лучший путь
            prompt = f"""
            Ты — ГИС-навигатор по графу знаний. 
            Цель пользователя: "{query}"
            Текущий узел: "{current_node_name}"
            Доступные переходы из этого узла:
            {chr(10).join(options)}
            
            Выбери НОМЕР наиболее полезного перехода, чтобы приблизиться к выполнению цели. 
            Если полезных переходов нет, ответь 'STOP'. 
            Ответь ТОЛЬКО цифрой или словом STOP.
            """
            
            # ВАЖНО: Тут мы используем LLM напрямую (можно добавить ее в __init__)
            choice = self.nav_llm.invoke(prompt).content.strip()

            if 'STOP' in choice.upper() or not choice.isdigit():
                break

            idx = int(choice)
            if idx >= len(neighbors): break

            # 4. Обновляем путь
            selected = neighbors[idx]
            path_triples.append({
                "from": current_node_name,
                "rel": selected['rel'],
                "to": selected['nName']
            })
            
            # Переходим к следующему узлу
            current_node_id = selected['neighbor']
            current_node_name = selected['nName']
            if current_node_id in visited: break # Защита от циклов
            visited.add(current_node_id)
            
            print(f"➡️ Шаг {step+1}: Переход в '{current_node_name}'")

        return path_triples
    def _get_all_entities(self):
        """Загрузка легковесного индекса всех узлов для векторизации."""
        query = self.prefixes + """
        SELECT DISTINCT ?id ?name ?category WHERE {
            ?id a ?realType .
            
            OPTIONAL { ?id wr_kz:Post_name ?postName . }
            OPTIONAL { ?id rdfs:label ?rdfsLabel . }
            BIND(COALESCE(?postName, ?rdfsLabel, REPLACE(STR(?id), "^.*[#/](.+)$", "$1")) AS ?name)
            
            BIND(REPLACE(STR(?realType), "^.*[#/](.+)$", "$1") AS ?category)
            
            FILTER(?category != "GroupNode")
        }
        """
        records = self.db.execute_query(query)
        return [{"id": r["id"], "name": r["name"], "category": r.get("category", "Unknown")} for r in records]
    def find_solution_subgraph(self, demand, top_k1=5, top_k2=15):
        """
        Главный пайплайн поиска GeoGraphRAG.
        """
        print("\n⚙️ [DGE] Запуск Dense Graph Extraction...")
        if demand.get("category") == "anomalous":
            self.logger.warning("🛑 Запрос заблокирован: обнаружена аномалия/выдуманный объект.")
            return [] # Возвращаем пустой граф!
        # --- PHASE I: Умный сбор ключевых слов ---
        search_queries = []
        
        # 1. Берем параметры (например, "уровень воды")
        inputs = demand.get('extracted_inputs', [])
        if isinstance(inputs, list):
            search_queries.extend(inputs)
        elif isinstance(inputs, str):
            search_queries.append(inputs)
            
        # 2. ОБЯЗАТЕЛЬНО берем целевую сущность (или НЕСКОЛЬКО сущностей!)
        target = demand.get('target_output', [])
        if isinstance(target, list):
            # Если LLM вернула список (["River A", "River B"])
            search_queries.extend([str(t) for t in target if str(t).lower() not in ["unknown", "none", ""]])
        elif isinstance(target, str) and target.lower() not in ["unknown", "none", ""]:
            # Если LLM вернула строку через запятую ("River A, River B")
            if ',' in target:
                search_queries.extend([t.strip() for t in target.split(',') if t.strip()])
            else:
                # Если там ровно одна река
                search_queries.append(target)
            
        # 3. Резервный вариант, если всё пустое
        if not search_queries:
            logic = demand.get('modeling_logic', '')
            if logic:
                search_queries.append(logic)

        # Очищаем от пустых значений и дубликатов
        search_queries = list(set([q for q in search_queries if q and len(str(q)) > 2]))

        if not search_queries:
            print("❌ [DEBUG] Запрос пуст, поиск невозможен.")
            return []

        all_entities = self._get_all_entities()
        triples = []
        seen = set()
        found_nodes = set()

        # --- PHASE II: Dense Graph Extraction (Векторный поиск по узлам) ---
        # --- PHASE II: Dense Graph Extraction (Векторный поиск по узлам) ---
        
        for query_text in search_queries:
            matches = self.embedder.find_top_matches(query_text, all_entities, top_k=top_k1)
            for match, score in matches:
                if score >= 0.83: 
                    node_id = match['id'] 
                    node_name = match['name']
                    found_nodes.add((node_id, node_name))
                    print(f"🎯 [DGE Match] Нашел узел: '{node_name}' (Уверенность: {score:.2f})")
                else:
                    print(f"⚠️ [DGE Skip] Узел '{match['name']}' отброшен ({score:.2f} < 0.83)")

        if not found_nodes:
            return []
        category = demand.get('category', 'explicit')
        if category == 'implicit':
            print(f"\n🧠 [Agentic Mode] Категория IMPLICIT. Запуск навигации...")
            # Берем первый найденный узел как стартовую точку для агента
            start_node_id, start_node_name = list(found_nodes)[0]
            
            # Запускаем итеративную навигацию
            nav_path = self.iterative_navigation(demand.get('modeling_logic', ''), start_node_id, start_node_name)
            
            # Добавляем найденный путь в общий список триплетов
            for t in nav_path:
                triples.append(t)
            print(f"✅ Агент проложил путь из {len(nav_path)} шагов.")


        # --- PHASE III: Subgraph Expansion (Поиск связей/путей) ---
        print(f"\n🕸️ [SSG] Расширение связей для {len(found_nodes)} узлов...")
        for node_id, node_name in found_nodes:
            expansion_query = self.prefixes + f"""
            SELECT ?sourceName ?rel ?targetName WHERE {{
                {{
                    <{node_id}> ?relUri ?target .
                    OPTIONAL {{ <{node_id}> wr_kz:Post_name|rdfs:label ?sLbl }}
                    OPTIONAL {{ ?target wr_kz:Post_name|rdfs:label ?tLbl }}
                    BIND(COALESCE(?sLbl, REPLACE(STR(<{node_id}>), "^.*[#/](.+)$", "$1")) AS ?sourceName)
                    BIND(COALESCE(?tLbl, REPLACE(STR(?target), "^.*[#/](.+)$", "$1")) AS ?targetName)
                }}
                UNION
                {{
                    ?source ?relUri <{node_id}> .
                    OPTIONAL {{ ?source wr_kz:Post_name|rdfs:label ?sLbl }}
                    OPTIONAL {{ <{node_id}> wr_kz:Post_name|rdfs:label ?tLbl }}
                    BIND(COALESCE(?sLbl, REPLACE(STR(?source), "^.*[#/](.+)$", "$1")) AS ?sourceName)
                    BIND(COALESCE(?tLbl, REPLACE(STR(<{node_id}>), "^.*[#/](.+)$", "$1")) AS ?targetName)
                }}
                BIND(REPLACE(STR(?relUri), "^.*[#/](.+)$", "$1") AS ?rel)
                FILTER(?rel NOT IN ("type", "hasInstance", "hasAnchor"))
            }} LIMIT {top_k2}
            """
            
            neighbors = self.db.execute_query(expansion_query)
            for res in neighbors:
                key = (res['sourceName'], res['rel'], res['targetName'])
                if key not in seen:
                    seen.add(key)
                    triples.append({
                        "from": res['sourceName'], "rel": res['rel'], 
                        "to": res['targetName'], "code": ""
                    })


 # --- PHASE IV: Deep Attributes Extraction (Глубокое извлечение атрибутов) ---
        print("\n📝 [Phase IV: Attributes] Извлекаем параметры узлов и их постов мониторинга...")
        for node_id, node_name in found_nodes:
            attr_query = self.prefixes + f"""
            SELECT ?sourceName ?p ?val WHERE {{
                {{
                    # Случай А: Прямые параметры самого объекта (например, длина реки)
                    <{node_id}> ?p ?val .
                    BIND("{node_name}" AS ?sourceName)
                    FILTER(isLiteral(?val)) 
                }}
                UNION
                {{
                    # Случай Б: Параметры постов (Observation), привязанных к объекту
                    ?obs sosa:hasFeatureOfInterest <{node_id}> .
                    ?obs ?p ?val .
                    FILTER(isLiteral(?val))
                    
                    # Склеиваем имя объекта и имя поста, чтобы LLM понимала, откуда цифры
                    OPTIONAL {{ ?obs wr_kz:Post_name|rdfs:label ?obsLbl }}
                    BIND(COALESCE(CONCAT("{node_name} | ", ?obsLbl), CONCAT("{node_name} | Пост мониторинга")) AS ?sourceName)
                }}
            }} LIMIT 50
            """
            attributes = self.db.execute_query(attr_query)
            for attr in attributes:
                rel_name = attr['p'].split('#')[-1].split('/')[-1]
                # Пропускаем WKT, так как мы берем его в Фазе V, и системные label
                if "asWKT" not in rel_name and rel_name != "label":
                    triples.append({
                        "from": attr['sourceName'], # Теперь тут будет "Ile River | Dobyn pier"
                        "rel": rel_name,
                        "to": str(attr['val']),
                        "code": "" 
                    })

        # --- PHASE V: Geo-Spatial Expansion (Склейка имени объекта и точки) ---
        print("\n🗺️ [Phase V: Geo-Spatial] Поиск гео-координат (WKT) для карты...")
        for node_id, node_name in found_nodes:
            geo_query = self.prefixes + f"""
            SELECT DISTINCT ?ptName ?wkt WHERE {{
                {{
                    # Случай 1: Координаты привязаны прямо к узлу
                    <{node_id}> geo:asWKT ?wkt .
                    BIND("{node_name}" AS ?ptName)
                }}
                UNION
                {{
                    # Случай 2: Координаты лежат в обсервациях, связанных с узлом
                    ?obs sosa:hasFeatureOfInterest <{node_id}> .
                    ?obs geo:asWKT ?wkt .
                    OPTIONAL {{ ?obs rdfs:label|wr_kz:Post_name ?obsLbl }}
                    
                    # ВАЖНО: Склеиваем имя реки и имя поста!
                    BIND(COALESCE(CONCAT("{node_name} | ", ?obsLbl), CONCAT("{node_name} | Точка мониторинга")) AS ?ptName)
                }}
            }} LIMIT 5
            """
            geo_results = self.db.execute_query(geo_query)
            for geo in geo_results:
                triples.append({
                    "from": geo['ptName'], # Формат: "Ile River | Dobyn pier"
                    "rel": "hasWKT",
                    "to": geo['wkt'],
                    "code": ""
                })
                print(f"📍 Найдена геометрия: {geo['ptName']} -> {geo['wkt']}")

        return triples