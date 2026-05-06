python
         import geopandas as gpd
         import folium
         # Load data
         data = {
             'name': ['Factory 1', 'Factory 2', ...],
             'water_consumption': [500, 300, ...],
             'geometry': [Point(x1, y1), Point(x2, y2), ...]
         }
         gdf = gpd.GeoDataFrame(data)
         # Create map
         m = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=10)
         # Add points to map
         for idx, row in gdf.iterrows():
             folium.CircleMarker(
                 location=[row['geometry'].y, row['geometry'].x],
                 radius=row['water_consumption']/50,
                 color='blue',
                 fill=True,
                 fill_color='blue'
             ).add_to(m)
         # Save map
         m.save("45.html")