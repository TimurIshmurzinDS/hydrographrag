python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Calculate water consumption intensity (water consumption per unit area of the basin)
   water_consumption = Water_consumption_Value  # Replace with actual value or data source
   basin_area = Basin_are_km²  # Replace with actual value or data source
   water_intensity = water_consumption / basin_area

   print(f"Water consumption intensity: {water_intensity} m³/km²")

   # Save the final map
   m.save("182.html")