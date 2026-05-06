python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin_data = gpd.read_file(r"data/basin_data.shp")
   basin_data = basin_data.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin_data.centroid.y.mean(), basin_data.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for Bayankol village (replace with actual data if available)
   villages = [{'name': 'Bayankol village', 'coordinates': wkt.loads('POINT (73.123456 53.123456)'} # Replace with actual coordinates

   # Add villages to the map
   for village in villages:
       folium.Marker(location=[village['coordinates'].y, village['coordinates'].x], popup=village['name']).add_to(m)

   # Save the final map
   m.save("151.html")