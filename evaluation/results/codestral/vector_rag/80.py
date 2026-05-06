python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map using the centroid of the shapefile
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing river names and coordinates (WKT)
   rivers = [{'name': 'Koktal River', 'coordinates': 'POINT (37.123456 55.123456)'},
             {'name': 'Tokyraun River', 'coordinates': 'POINT (38.123456 56.123456)'},
             {'name': 'Koksu River', 'coordinates': 'POINT (39.123456 57.123456)'}]

   # Add rivers to the map
   for river in rivers:
       folium.Marker(location=wkt.loads(river['coordinates']).coords[0], popup=river['name'], icon=folium.Icon(color='blue')).add_to(m)

   # Save the final map
   m.save("80.html")