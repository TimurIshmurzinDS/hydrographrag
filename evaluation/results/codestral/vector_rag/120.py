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

   # Hardcoded data for rivers and water consumption in the village Lepsy
   rivers = [{'name': 'Kurty River', 'water_level': Water_level_Value}, {'name': 'Lepsy River', 'water_level': Water_level_Value}]
   water_consumption = {'village': 'аул Lepsy', 'consumption': Water_consumption_Value}

   # Calculate total water volume in rivers
   total_river_volume = sum([river['water_level'] for river in rivers])

   # Check if the total water volume is sufficient to meet the water consumption of the village Lepsy
   if total_river_volume >= water_consumption['consumption']:
       print("The total water volume from Kurty River and Lepsy River is sufficient to meet the water consumption of аул Lepsy.")
   else:
       print("The total water volume from Kurty River and Lepsy River is not sufficient to meet the water consumption of аул Lepsy.")

   # Save the final map
   m.save("120.html")