python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers and their water levels (replace with actual data)
   rivers = [{'name': 'Shyzhyn River', 'water_level': 10}, {'name': 'Sarykan River', 'water_level': 8}]

   # Add markers for each river on the map
   for river in rivers:
       folium.Marker(location=[river['lat'], river['lon']], popup=f"{river['name']}: Water Level - {river['water_level']} m").add_to(m)

   # Save the final map
   m.save("165.html")