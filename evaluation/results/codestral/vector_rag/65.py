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

   # Hardcoded data for water level and date of measurement
   data = [
       {"river": "Aksu River", "water_level": None, "date": "2023-01-01"},
       {"river": "Byzhy River", "water_level": 5.6, "date": "2023-01-01"}
   ]

   # Check water level and sensor status
   for entry in data:
       if entry["water_level"] is None:
           print(f"Sensor on {entry['river']} seems to be malfunctioning at date {entry['date']}")
       else:
           print(f"Water level on {entry['river']} at date {entry['date']} is {entry['water_level']} meters")

   # Save the final map
   m.save("65.html")