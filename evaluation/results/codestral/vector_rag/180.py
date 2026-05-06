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

   # Hardcoded list of dictionaries for rivers' coordinates (WKT)
   # This section would be filled with actual data if available
   rivers = [
       {'name': 'Tekes River', 'coordinates': 'POINT (0 0)'},
       {'name': 'Sarykan River', 'coordinates': 'POINT (0 0)'}
   ]

   # Add rivers to the map
   for river in rivers:
       folium.GeoJson(wkt.loads(river['coordinates']), style_function=lambda x: {'color': 'blue'}).add_to(m)

   # Save the final map
   m.save("180.html")