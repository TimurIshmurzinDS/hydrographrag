python
         import geopandas as gpd
         from shapely.geometry import Point, LineString
         import folium
         # Load data
         emel = gpd.read_file('emel.geojson')
         tentek = gpd.read_file('tentek.geojson')
         # Find intersection points
         intersections = []
         for i in range(len(emel)):
             for j in range(len(tentek)):
                 if emel['geometry'][i].intersects(tentek['geometry'][j]):
                     intersections.append(emel['geometry'][i].intersection(tentek['geometry'][j]))
         # Create new GeoDataFrame with intersection points
         gdf = gpd.GeoDataFrame(geometry=intersections)
         # Visualize results on map
         m = folium.Map(location=[gdf['geometry'].y.mean(), gdf['geometry'].x.mean()], zoom_start=10)
         for idx, row in gdf.iterrows():
             folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=5, color='red').add_to(m)
         m.save("174.html")