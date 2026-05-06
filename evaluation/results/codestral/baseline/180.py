python
        import geopandas as gpd
        import networkx as nx
        import folium

        # Load data
        tekes = gpd.read_file('tekes.geojson')
        sarykan = gpd.read_file('sarykan.geojson')

        # Create a graph from the rivers data
        G = nx.Graph()

        for river in [tekes, sarykan]:
            for idx, row in river.iterrows():
                coords = list(row['geometry'].coords)
                for i in range(len(coords)-1):
                    G.add_edge(coords[i], coords[i+1])

        # Analyze the network
        # Here you can add your own analysis code, e.g., finding bottlenecks, turns, etc.

        # Visualize the results on a map
        m = folium.Map(location=[tekes['geometry'].centroid.y.mean(), tekes['geometry'].centroid.x.mean()], zoom_start=10)

        for edge in G.edges():
            folium.PolyLine([edge[0][::-1], edge[1][::-1]], color="blue", weight=2.5, opacity=1).add_to(m)

        m.save("180.html")