python
         import geopandas as gpd
         from shapely.geometry import Point, LineString
         import networkx as nx
         import folium
         # Load data
         river = gpd.read_file('karaoy_river.shp')
         # Create grid or network for pathfinding
         G = nx.Graph()
         for i, row in river.iterrows():
             coords = list(row['geometry'].coords)
             for j in range(len(coords)-1):
                 p1 = Point(coords[j])
                 p2 = Point(coords[j+1])
                 G.add_edge(p1, p2, weight=p1.distance(p2))
         # Define start and end points
         start = Point(river['geometry'].iloc[0].coords[0])
         end = Point(river['geometry'].iloc[-1].coords[-1])
         # Find shortest path
         path = nx.shortest_path(G, source=start, target=end, weight='weight')
         # Visualize results
         m = folium.Map(location=[river['geometry'].centroid.y, river['geometry'].centroid.x], zoom_start=10)
         folium.GeoJson(river).add_to(m)
         folium.PolyLine(locations=[(p.y, p.x) for p in path], color='red').add_to(m)
         m.save("224.html")