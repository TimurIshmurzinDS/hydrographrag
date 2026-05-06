python
         import folium
         from pyproj import Transformer
         import networkx as nx
         # Assuming you have a DataFrame 'df' with columns 'from', 'to', and 'distance' representing the river network
         G = nx.from_pandas_edgelist(df, 'from', 'to', edge_attr='distance')
         source = 'Киши-Осек'
         paths = nx.single_source_dijkstra_path(G, source)
         # Assuming you have a DataFrame 'coordinates' with columns 'river' and 'coordinates' representing the coordinates of each river
         m = folium.Map()
         for target in paths:
             if target != source:
                 path = paths[target]
                 coords = [coordinates.loc[coordinates['river'] == river, 'coordinates'].values[0] for river in path]
                 transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
                 coords = [transformer.transform(lat, lon) for lat, lon in coords]
                 folium.PolyLine(coords, color="red").add_to(m)
         m.save("179.html")