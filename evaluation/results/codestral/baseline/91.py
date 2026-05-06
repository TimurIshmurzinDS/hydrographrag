python
        import osmnx as ox
        import networkx as nx
        import folium

        # Load the street network of the area around river Urzhara
        G = ox.graph_from_place('Уржар, Россия', network_type='drive')

        # Convert the graph to a directed graph where edges point from source to sink
        G = nx.DiGraph(G)

        # Find all nodes that have more than one incoming edge and less than one outgoing edge (i.e., tributaries of river Urzhara)
        tributaries = [node for node in G.nodes if G.in_degree(node) > 1 and G.out_degree(node) < 1]

        # Get the coordinates of each tributary
        tributaries_coords = ox.utils_graph.node_gdf(G, nodes=tributaries)[['y', 'x']].values.tolist()

        # Visualize the results on a map using folium
        m = folium.Map(location=[sum([coord[0] for coord in tributaries_coords]) / len(tributaries_coords),
                                 sum([coord[1] for coord in tributaries_coords]) / len(tributaries_coords)], zoom_start=12)
        for coord in tributaries_coords:
            folium.CircleMarker(location=coord, radius=5).add_to(m)
        m.save("91.html")