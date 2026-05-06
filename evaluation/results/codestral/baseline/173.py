python
         import folium
         from pyproj import Transformer
         import networkx as nx
         # Assuming you have a GeoDataFrame 'gdf' with the river network data
         # Convert coordinates to Web Mercator (EPSG:3857) for use in Folium
         transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
         gdf['geometry'] = gdf['geometry'].apply(lambda geom: transformer.transform(geom.x, geom.y))
         # Create a directed graph from the GeoDataFrame
         G = nx.from_pandas_edgelist(gdf, 'from_node', 'to_node')
         # Find the node corresponding to the Shynzhal River
         start_node = gdf[gdf['name'] == 'Shynzhal'].iloc[0]['from_node']
         # Find the shortest path to major river systems
         paths = nx.shortest_path(G, source=start_node)
         # Create a Folium map centered around the Shynzhal River
         m = folium.Map(location=[gdf[gdf['name'] == 'Shynzhal'].iloc[0]['geometry'].y, gdf[gdf['name'] == 'Shynzhal'].iloc[0]['geometry'].x], zoom_start=12)
         # Add the river network to the map
         for _, row in gdf.iterrows():
             folium.PolyLine(locations=[(p.y, p.x) for p in row['geometry'].coords], color='blue').add_to(m)
         # Add the shortest path to major river systems to the map
         for node in paths:
             if gdf[gdf['from_node'] == node]['name'].values[0] in ['Main River System 1', 'Main River System 2', ...]:
                 folium.PolyLine(locations=[(p.y, p.x) for p in gdf[gdf['from_node'] == node].iloc[0]['geometry'].coords], color='red').add_to(m)
         # Save the map as an HTML file
         m.save("173.html")