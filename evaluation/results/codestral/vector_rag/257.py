python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Define the critical water level for Bayankol River and current water level (replace with actual data)
   critical_water_level = 10.0  # meters
   current_water_level = 9.5  # meters

   # Calculate irrigation needs based on water levels
   if current_water_level < critical_water_level:
       irrigation_needed = True
       # Calculate the volume of irrigation water needed (replace with actual calculation)
       irrigation_volume = 1000.0  # cubic meters
   else:
       irrigation_needed = False
       irrigation_volume = 0.0

   # Print the results
   print(f"Irrigation needed: {irrigation_needed}")
   print(f"Volume of irrigation water needed: {irrigation_volume} cubic meters")

   # Save the final map
   m.save("257.html")