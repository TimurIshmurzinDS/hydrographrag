python
         import geopandas as gpd
         import networkx as nx
         import folium
         # Load data
         rivers = gpd.read_file('rivers.geojson')
         # Create topological connection
         rivers['from'] = rivers.geometry.apply(lambda x: x.boundary[0])
         rivers['to'] = rivers.geometry.apply(lambda x: x.boundary[-1])
         # Create graph
         G = nx.Graph()
         for idx, row in rivers.iterrows():
             G.add_edge(row['from'], row['to'], attr_dict=row)
         # Find tributaries of the Emel river
         emel_node = rivers[rivers['name'] == 'Емель']['to'].iloc[0]
         tributaries = nx.dfs_tree(G, source=emel_node)
         tributaries = [trib for trib in tributaries if trib != emel_node]
         # Visualize results on map
         m = folium.Map()
         for node in G.nodes:
             folium.PolyLine(locations=[(y, x) for x, y in node.coords], color='blue').add_to(m)
         for trib in tributaries:
             if rivers[rivers['to'] == trib]['name'].iloc[0] in ['Тентек', 'Быж']:
                 folium.PolyLine(locations=[(y, x) for x, y in trib.coords], color='red').add_to(m)
         m.save("101.html")