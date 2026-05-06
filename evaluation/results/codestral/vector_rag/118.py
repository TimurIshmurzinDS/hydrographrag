python
   import geopandas as gpd
   import folium
   from shapely.wkt import loads

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for river and village locations (replace with actual data)
   locations = [{'name': 'Sarykan River', 'coordinates': 'POINT(...)'}, {'name': 'Temirlik River', 'coordinates': 'POINT(...)'}, {'name': 'Temirlik village', 'coordinates': 'POINT(...)'}]

   # Add rivers and village to the map
   for location in locations:
       point = loads(location['coordinates'])
       folium.Marker([point.y, point.x], popup=location['name']).add_to(m)

   # Save the final map
   m.save("118.html")