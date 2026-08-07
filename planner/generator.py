import os
from langchain_ollama import ChatOllama

class SolutionPlanner:
    """
    Модуль для генерации планов моделирования и кода.
    Адаптирован для честного Ablation Study:
    Базовые модели и GeoGraphRAG используют единые шаблоны и правила OOD.
    """
    def __init__(self, model_name="qwen2.5-coder:7b"):
        # Температура 0 для максимальной детерминированности
        self.llm = ChatOllama(model=model_name, temperature=0)
        self.shp_path = "data/basin_data.shp"

    def _get_unified_prompt(self, user_query, context_type, context_data, points_list_str, query_id, use_ood_rule=True, use_template=True):
        prompt = f"""
        You are a professional GIS and Hydrology Expert Assistant.
        User Query: "{user_query}"
        
        Context provided ({context_type}): 
        {context_data}
        """
        
        if use_ood_rule:
            prompt += """
        CRITICAL ABSTENTION RULE (OOD REJECTION):
        If the user query is NOT related to hydrology, basin analysis, or geospatial mapping in Kazakhstan (e.g., recipes, crypto, space, random coding), you MUST reject it.
        Output EXACTLY this format and nothing else:
        ### Modeling Solution: 
        ОТКАЗ: Запрос не относится к гидрологии бассейна.
        ### Implementation Code: 
        # ОТКАЗ: Запрос не относится к гидрологии бассейна.
        """

        prompt += """
        If the query IS valid, follow these STRICT INSTRUCTIONS:
        1. STRICT STRUCTURE: Answer strictly with "### Modeling Solution:" followed by the text, and then "### Implementation Code:" followed by the Python code.
        2. LANGUAGE: The "Modeling Solution" text MUST be in the same language as the User Query. Write a cohesive analytical narrative.
        3. MISSING ENTITIES: If no useful info is provided in the context to solve the task, state: "Информации недостаточно для полного анализа."
        """

        if use_template:
            prompt += f"""
        STRICT CODE PIPELINE (COPY AND PASTE THIS EXACT BASE CODE, ONLY FILL IN THE 'points' ARRAY IF NEEDED):
        ```python
        import geopandas as gpd
        import folium
        from shapely import wkt

        # 1. Load basin
        basin_data = gpd.read_file(r"{self.shp_path}").to_crs('EPSG:4326')
        centroid = basin_data.geometry.centroid.iloc[0]
        
        # 2. Init map
        m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
        folium.GeoJson(basin_data.to_json(), style_function=lambda x: {{'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}}).add_to(m)

        # 3. Add points
        # Array of dicts with "name" and "wkt" coordinates.
        points = {points_list_str}
        
        # 4. Draw markers
        for p in points:
            try:
                geom = wkt.loads(p["wkt"])
                folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)
            except Exception:
                pass

        m.save("{query_id}.html")
        ```
        """
        else:
            prompt += f"""
        IMPLEMENTATION INSTRUCTIONS:
        Write the implementation code yourself from scratch. You must use `geopandas` and `folium`.
        Use `{self.shp_path}` for the basin boundary. 
        Save the final map strictly as `m.save("{query_id}.html")`.
        """
        
        return prompt

    def generate_response(self, user_query, query_id, mode_type, context_data=None, use_ood_rule=True, use_template=True):
        if mode_type == "baseline":
            c_type = "Internal Memory (Zero-shot)"
            c_data = "Use your internal knowledge. No external context provided."
            pts = "[] # GUESSED WKT COORDINATES"
        elif mode_type == "vector_rag":
            c_type = "Text Document Chunks"
            c_data = context_data
            pts = "[] # EXTRACTED WKT COORDINATES"
        else: # geographrag
            c_type = "Graph Knowledge (Triples)"
            
            text_triples = [t for t in context_data if t.get('rel') != 'hasWKT']
            text_triples.sort(key=lambda x: ("Population" in x['rel']))
            c_data = " ".join([f"Step {i+1}: {t['from']} -[{t['rel']}]-> {t['to']}." for i, t in enumerate(text_triples[:35])])
            
            wkt_triples = [t for t in context_data if t.get('rel') == 'hasWKT']
            pts = "[\n"
            for pt in wkt_triples:
                safe_name = str(pt['from']).replace('"', '\\"')
                safe_wkt = str(pt['to']).replace('"', '\\"')
                pts += f'            {{"name": "{safe_name}", "wkt": "{safe_wkt}"}},\n'
            pts += "        ]"

        prompt = self._get_unified_prompt(user_query, c_type, c_data, pts, query_id, use_ood_rule, use_template)
        return self.llm.invoke(prompt).content

    def generate(self, mode, user_query, query_id, context_data=None, use_ood_rule=True, use_template=True):
        return self.generate_response(user_query, query_id, mode, context_data, use_ood_rule, use_template)