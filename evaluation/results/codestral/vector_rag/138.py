python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for observations (replace with actual data)
   observations = [{'name': 'Butak River Observation', 'water_level': None, 'date': None, 'geometry': wkt.loads('POINT (longitude latitude)')},
                  {'name': 'Osek River Confluence Observation', 'water_level': None, 'date': None, 'geometry': wkt.loads('POINT (longitude latitude)')}]

   # Add observations to the map
   for observation in observations:
       folium.Marker(location=[observation['geometry'].y, observation['geometry'].x], popup=observation['name']).add_to(m)

   # Save the final map
   m.save("138.html")