python
         import geopandas as gpd
         import networkx as nx
         from shapely.geometry import Point, LineString
         import folium
         # Load river data
         rivers = gpd.read_file('rivers.shp')
         # Create graph nodes and edges
         G = nx.Graph()
         for i, row in rivers.iterrows():
             coords = list(row['geometry'].coords)
             for j in range(len(coords)):
                 if j == 0:
                     prev_node = Point(coords[j])
                     G.add_node(prev_node, pos=(coords[j][1], coords[j][0]))
                 else:
                     curr_node = Point(coords[j])
                     G.add_node(curr_node, pos=(coords[j][1], coords[j][0]))
                     G.add_edge(prev_node, curr_node, weight=LineString([prev_node, curr_node]).length)
                     prev_node = curr_node
         # Find shortest path between Teke and Tentek rivers
         teke_node = None
         tentek_node = None
         for node in G.nodes:
             if rivers[rivers['name'] == 'Teke'].distance(Point(node)).min() < 1e-6:
                 teke_node = node
             elif rivers[rivers['name'] == 'Tentek'].distance(Point(node)).min() < 1e-6:
                 tentek_node = node
         shortest_path = nx.shortest_path(G, source=teke_node, target=tentek_node, weight='weight')
         # Calculate total length of the path
         total_length = sum([G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1)])
         print('Total length:', total_length, 'meters')
         # Visualize the result on a map
         m = folium.Map(location=[55, 37], zoom_start=6)
         for i in range(len(shortest_path)-1):
             folium.PolyLine([G.nodes[shortest_path[i]]['pos'], G.nodes[shortest_path[i+1]]['pos']], color='blue').add_to(m)
         m.save('167.html')