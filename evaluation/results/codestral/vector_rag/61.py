python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for water level sensors on Aksu River
   water_level_sensors = [
       {"name": "Sensor 1", "coordinates": wkt.loads('POINT (69.30528 40.07496)'), "water_level": Water_level_Value, "date": Date_water_level_Value},
       # Add more sensors as needed
   ]

   # Add water level sensors to the map
   for sensor in water_level_sensors:
       folium.Marker(location=[sensor['coordinates'].y, sensor['coordinates'].x], popup=f"Sensor: {sensor['name']}<br>Water Level: {sensor['water_level']} cm<br>Date: {sensor['date']}", icon=folium.Icon(color='blue')).add_to(m)

   # Save the final map
   m.save("61.html")