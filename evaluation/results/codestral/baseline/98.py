python
         import osmnx as ox
         import geopandas as gpd
         import folium
         # Set the place name or bounding box for your region of interest
         place = "Your Region"
         # Download river data from OpenStreetMap
         rivers_gdf = ox.geocode_to_gdf({'query': place, 'which_result': 1})
         rivers_gdf = rivers_gdf[rivers_gdf['waterway'].isin(['river', 'stream'])]
         # Filter the data to include only Tenteck and Byzh rivers
         rivers_gdf = rivers_gdf[rivers_gdf['name'].isin(['Тентек', 'Быж'])]
         # Download basins data (you may need to find a suitable source)
         basins_gdf = gpd.read_file("path/to/basins/data")
         # Determine which basin each river flows into
         rivers_gdf['basin'] = None
         for i, river in rivers_gdf.iterrows():
             for j, basin in basins_gdf.iterrows():
                 if river['geometry'].intersects(basin['geometry']):
                     rivers_gdf.at[i, 'basin'] = basin['name']
         # Visualize the results on a map using folium
         m = folium.Map(location=[rivers_gdf['geometry'].centroid.y.mean(), rivers_gdf['geometry'].centroid.x.mean()], zoom_start=10)
         for i, river in rivers_gdf.iterrows():
             folium.GeoJson(river['geometry'].__geo_interface__, style_function=lambda x: {'color': 'blue'}).add_to(m)
             folium.Marker([river['geometry'].centroid.y, river['geometry'].centroid.x], popup=f"{river['name']} flows into {river['basin']} basin").add_to(m)
         for i, basin in basins_gdf.iterrows():
             folium.GeoJson(basin['geometry'].__geo_interface__, style_function=lambda x: {'color': 'green', 'fillOpacity': 0.1}).add_to(m)
         m.save("98.html")