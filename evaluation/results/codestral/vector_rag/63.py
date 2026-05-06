python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize the map with the centroid of the basin
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with hydro posts data (coordinates and water levels)
   hydro_posts = [
       {"name": "Hydro Post 1", "coordinates": "POINT (50.4501 30.5234)", "water_level": 100},
       {"name": "Hydro Post 2", "coordinates": "POINT (50.4602 30.5335)", "water_level": 98},
       # Add more hydro posts as needed
   ]

   # Add hydro posts to the map with water level information
   for post in hydro_posts:
       folium.Marker(location=[wkt.loads(post['coordinates']).y, wkt.loads(post['coordinates']).x], popup=f"{post['name']}: {post['water_level']} cm").add_to(m)

   # Save the final map
   m.save("63.html")