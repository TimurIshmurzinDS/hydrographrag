python
         import networkx as nx
         import folium
         from shapely.geometry import LineString, Point
         # Загрузка данных о речной сети (предполагается, что они уже загружены в переменную rivers_data)
         G = nx.Graph()
         for river in rivers_data:
             start_node = Point(river['start']['lon'], river['start']['lat'])
             end_node = Point(river['end']['lon'], river['end']['lat'])
             G.add_edge(start_node, end_node, weight=river['length'])
         # Определение топологии притоков реки Тентек
         tenteck_tributaries = [river for river in rivers_data if river['end']['name'] == 'Tenteck']
         tribute_graph = nx.Graph()
         for tribute in tenteck_tributaries:
             start_node = Point(tribute['start']['lon'], tribute['start']['lat'])
             end_node = Point(tribute['end']['lon'], tribute['end']['lat'])
             tribute_graph.add_edge(start_node, end_node, weight=tribute['length'])
         # Оценка влияния топологии притоков реки Тентек на общую структуру речной сети региона
         degree_centrality = nx.degree_centrality(G)
         tribute_degree_centrality = nx.degree_centrality(tribute_graph)
         # Визуализация результатов на карте
         m = folium.Map(location=[55, 37], zoom_start=6)
         for edge in G.edges():
             line = LineString([edge[0], edge[1]])
             folium.PolyLine(locations=line.coords[:], color='blue').add_to(m)
         for edge in tribute_graph.edges():
             line = LineString([edge[0], edge[1]])
             folium.PolyLine(locations=line.coords[:], color='red').add_to(m)
         m.save("178.html")