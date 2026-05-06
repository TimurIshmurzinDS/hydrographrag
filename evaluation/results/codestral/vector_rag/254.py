python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import random

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing coordinates (WKT)
   observations = [{'name': 'Shilik River Observation', 'coordinates': 'POINT (69.178345 42.302783)'}]

   # Convert WKT to Shapely geometry and add to the map
   for observation in observations:
       geometry = wkt.loads(observation['coordinates'])
       folium.Marker([geometry.y, geometry.x], popup=observation['name']).add_to(m)

   # Generate a random number based on the river's sinuosity (placeholder code)
   # Replace this with actual calculation based on river geometry data
   sinuosity = 1.5  # placeholder value
   random_number = random.uniform(0, sinuosity)

   print("Generated random number:", random_number)

   # Save the final map
   m.save("254.html")