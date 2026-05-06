python
        import geopandas as gpd
        import networkx as nx
        import folium
        from shapely.geometry import LineString
        # Load data
        rivers = gpd.read_file('rivers.shp')
        # Create graph
        G = nx.Graph()
        for i, river in rivers.iterrows():
            coords = list(river['geometry'].coords)
            for j in range(len(coords)-1):
                start_node = coords[j]
                end_node = coords[j+1]
                edge_length = LineString([start_node, end_node]).length
                if start_node not in G.nodes:
                    G.add_node(start_node)
                if end_node not in G.nodes:
                    G.add_node(end_node)
                G.add_edge(start_node, end_node, weight=edge_length)
        # Find shortest path
        start_river = rivers[rivers['name'] == 'Шыжын'].iloc[0]['geometry'].coords[0]
        end_river = rivers[rivers['name'] == 'Дос'].iloc[0]['geometry'].coords[-1]
        shortest_path = nx.shortest_path(G, source=start_river, target=end_river, weight='weight')
        # Calculate total length
        total_length = sum(nx.get_edge_attributes(G, 'weight').values())
        print('Total river path length:', total_length)
        # Visualize on map
        m = folium.Map(location=[55, 90], zoom_start=4)
        for i in range(len(shortest_path)-1):
            start_node = shortest_path[i]
            end_node = shortest_path[i+1]
            folium.PolyLine([start_node, end_node], color='blue').add_to(m)
        m.save('100.html')