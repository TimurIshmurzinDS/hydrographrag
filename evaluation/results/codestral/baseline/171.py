python
         import geopandas as gpd
         import networkx as nx
         from shapely.geometry import Point, LineString
         import folium
         from scipy.spatial import cKDTree

         # Load data
         kishi_osek = gpd.read_file('path_to_kishi_osek_data')
         talgar = gpd.read_file('path_to_talgar_data')

         # Find intersection points
         intersection_points = []
         for i in range(len(kishi_osek)):
             for j in range(len(talgar)):
                 if kishi_osek['geometry'][i].intersects(talgar['geometry'][j]):
                     intersection_points.append(kishi_osek['geometry'][i].intersection(talgar['geometry'][j]))

         # Create a hydrographic network
         G = nx.Graph()
         for point in intersection_points:
             G.add_node(point)

         all_nodes = list(G.nodes()) + [Point(p) for p in kishi_osek['geometry'].apply(lambda x: x.coords[:]).explode().tolist()] + [Point(p) for p in talgar['geometry'].apply(lambda x: x.coords[:]).explode().tolist()]
         tree = cKDTree([(node.x, node.y) for node in all_nodes])

         for i in range(len(all_nodes)):
             _, indices = tree.query(all_nodes[i], k=2)
             for j in indices:
                 if i != j and all_nodes[i].distance(all_nodes[j]) < 1000: # Adjust the distance threshold as needed
                     G.add_edge(all_nodes[i], all_nodes[j], weight=all_nodes[i].distance(all_nodes[j]))

         # Calculate hydrogeomorphic distance
         start_node = intersection_points[0] # Assuming the first intersection point is the starting point for calculation
         distances = nx.single_source_dijkstra_path_length(G, start_node)

         end_node = min([node for node in distances if node != start_node], key=distances.get) # The endpoint is the closest node to the starting point
         hydrogeomorphic_distance = distances[end_node]

         print("Hydrogeomorphic distance: ", hydrogeomorphic_distance)

         # Visualize results on a map
         m = folium.Map(location=[55, 73], zoom_start=10)
         for node in G.nodes():
             folium.CircleMarker([node.y, node.x], radius=2).add_to(m)
         for edge in G.edges():
             line = LineString([edge[0], edge[1]])
             folium.PolyLine(locations=[[p.y, p.x] for p in line.coords]).add_to(m)
         m.save("171.html")