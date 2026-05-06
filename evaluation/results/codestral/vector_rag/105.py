python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers and their coordinates (WKT format)
   # This data is not provided in the context, so it's hardcoded as an example
   rivers = [
       {'name': 'Ulken Almaty River', 'coordinates': 'POINT(76.9482 43.1556)'},
       {'name': 'Emel River', 'coordinates': 'POINT(76.9500 43.1560)'},
       {'name': 'Tentek River', 'coordinates': 'POINT(76.9485 43.1552)'}
   ]

   # Add rivers to the map
   for river in rivers:
       folium.Marker([wkt.loads(river['coordinates']).y, wkt.loads(river['coordinates']).x], popup=river['name'], icon=folium.Icon(color='blue')).add_to(m)

   # Save the final map
   m.save("105.html")