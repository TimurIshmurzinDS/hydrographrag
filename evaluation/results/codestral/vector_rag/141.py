python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin_data = gpd.read_file(r"data/basin_data.shp")
       basin_data = basin_data.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries with water level data (replace this with actual data)
       water_level_data = [{'river': 'River1', 'water_classification': 'CRITICAL'}, {'river': 'River2', 'water_classification': 'NORMAL'}]

       # Add markers for rivers with critical water levels
       for river in water_level_data:
           if river['water_classification'] == 'CRITICAL':
               folium.Marker(location=[0, 0], popup=river['river'], icon=folium.Icon(color='red')).add_to(m)

       # Save the final map
       m.save("141.html")