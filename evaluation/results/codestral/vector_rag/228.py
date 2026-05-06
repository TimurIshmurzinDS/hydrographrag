python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map using the centroid of the shapefile
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with river coordinates (WKT)
   rivers = [{'name': 'Ayagoz River', 'coordinates': 'POINT (68.947351 45.002002)'}]

   # Add rivers to the map
   for river in rivers:
       coords = wkt.loads(river['coordinates'])
       folium.Marker([coords.y, coords.x], popup=river['name']).add_to(m)

   # Save the final map
   m.save("228.html")