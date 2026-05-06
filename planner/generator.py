import os
from langchain_ollama import ChatOllama

class SolutionPlanner:
    """
    Модуль для генерации планов моделирования и кода.
    Реализует фазу Graph-driven solution planning 
    и поддерживает базовые методы сравнения.
    """
    def __init__(self, model_name="qwen2.5-coder:7b"):
        self.llm = ChatOllama(model=model_name, temperature=0)
        
        # ПРИНУДИТЕЛЬНО задаем относительный путь для песочницы!
        self.shp_path = "data/basin_data.shp"

    def generate_io_response(self, user_query, query_id):
        prompt = f"""
        Suppose you are a professional GIS expert. 
        Geospatial modeling task: "{user_query}"
        
        Please generate a modeling solution and implementation code in Python.
        If visualization on a map is required, use the `folium` library and save the final map strictly as: `m.save("{query_id}.html")`.
        
        Output format:
        ### Modeling Solution: 
        (Natural language steps in RUSSIAN or English depending on the user query)
        ### Implementation Code: 
        (Complete Python script)
        """
        response = self.llm.invoke(prompt)
        return response.content

    def generate_cot_response(self, user_query, query_id):
        prompt = f"""
        Suppose you are a professional GIS expert. 
        Geospatial modeling task: "{user_query}"
        
        Instructions:
        1. Think step-by-step to construct the modeling solution.
        2. Develop clean Python code.
        3. Verify logic and syntax.
        4. If visualization on a map is required, use the `folium` library and save the final map strictly as: `m.save("{query_id}.html")`.
        
        Output format:
        ### Modeling Solution: 
        (Natural language steps in RUSSIAN or English depending on the user query)
        ### Implementation Code: 
        (Complete Python script)
        """
        response = self.llm.invoke(prompt)
        return response.content

    def generate_vector_rag_response(self, user_query, vector_context, query_id):
        prompt = f"""
        You are a strict, professional GIS and Hydrology Expert System.
        Context: {vector_context}
        Task: "{user_query}"
        
        CRITICAL INSTRUCTIONS:
        1. STRICT STRUCTURE: Answer strictly with "### Modeling Solution:" followed by the text, and then "### Implementation Code:" followed by the Python code.
        2. LANGUAGE: The "Modeling Solution" text MUST be in professional language DEPENDS ON THE LANGUAGE OF THE USER QUERY.
        3. MAXIMIZE DETAILS: Write a detailed description of the entities found in the context.
        4. PYTHON CODE RULES (CRITICAL FATAL ERRORS TO AVOID):
            - START your code by importing: `import geopandas as gpd`, `import folium`, `from shapely import wkt`.
            - FATAL ERROR 1: DO NOT try to read points or river names from the `{self.shp_path}` file. That file ONLY contains the exterior polygon boundaries of the basin.
            - FATAL ERROR 2: Save the final map strictly using a string filename: `m.save("{query_id}.html")`. DO NOT use undefined variables like `output_filename`.
            
            - CODE STRUCTURE: 
              a) Load the shapefile strictly using a raw string: `gpd.read_file(r"{self.shp_path}")`. Convert to CRS 'EPSG:4326'.
                 Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'.
                 Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2).
              b) If the context contains Coordinates (WKT), create a hardcoded list of dictionaries.
              c) SAVE the final map: `m.save("{query_id}.html")`.

        Output format:
        ### Modeling Solution: 
        (Detailed Russian analytical report or English if the user query is in English)
        ### Implementation Code: 
        (Correct Python script following the rules)
        """
        return self.llm.invoke(prompt).content
    
    def generate_geographrag_response(self, user_query, solution_triples, query_id):
        graph_context = ""
        for i, t in enumerate(solution_triples):
            graph_context += f"Step {i+1}: {t['from']} -[{t['rel']}]-> {t['to']}. "
            if t.get('code'):
                graph_context += f"Reference snippet: {t['code']}\n"

        prompt = f"""
        You are a strict, professional GIS and Hydrology Expert System.
        User Query: "{user_query}"
        
        Available Graph Knowledge (Triples):
        {graph_context}

        CRITICAL INSTRUCTIONS:
        1. STRICT STRUCTURE: Answer strictly with "### Modeling Solution:" and "### Implementation Code:".
        2. LANGUAGE: The "Modeling Solution" text MUST be in professional language DEPENDS ON THE LANGUAGE OF THE USER QUERY.
        3. SEPARATE DATA FROM CODE (CRITICAL): 
           - In the "Modeling Solution": Describe all found data (Water levels, Population, Area, etc.) using bullet points.
           - In the "Implementation Code": Use ONLY WKT coordinates to draw markers. DO NOT put other sensor data, ranges, or numeric arrays into the code.
        4. MISSING ENTITIES: For entities missing from the graph, add: "К сожалению, в базе данных графа отсутствуют данные" or "Unfortunately, the graph database is missing data".

        STRICT CODE PIPELINE (COPY AND PASTE THIS EXACT BASE CODE):
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

        # 3. Add YOUR points here based on Graph Knowledge
        points = [
            # Example: {{"name": "River Name", "wkt": "POINT(76.0 43.0)"}}
        ]
        
        # 4. Draw markers
        for p in points:
            geom = wkt.loads(p["wkt"])
            folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

        m.save("{query_id}.html")
        ```
        
        Output format:
        ### Modeling Solution: 
        (Detailed Russian analytical report or English if the user query is in English)
        ### Implementation Code: 
        (Correct Python script strictly following the COPY-PASTE template)
        """
        response = self.llm.invoke(prompt)
        return response.content

    def generate(self, mode, user_query, query_id, triples=None):
        if mode == "io":
            return self.generate_io_response(user_query, query_id)
        elif mode == "cot":
            return self.generate_cot_response(user_query, query_id)
        elif mode == "geographrag":
            return self.generate_geographrag_response(user_query, triples, query_id)
        elif mode == "vector_rag":
            return self.generate_vector_rag_response(user_query, triples, query_id)
        else:
            raise ValueError(f"Unknown mode: {mode}")