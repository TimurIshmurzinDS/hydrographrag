python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers (WKT coordinates are not provided in the context)
   rivers = [{'name': 'Kurty River'}, {'name': 'Urzhar River'}, {'name': 'Byzhy River'}]

   # Add rivers to the map (without specific coordinates, they will be represented as markers at the basin centroid)
   for river in rivers:
       folium.Marker(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], popup=river['name']).add_to(m)

   # Save the final map
   m.save("112.html")