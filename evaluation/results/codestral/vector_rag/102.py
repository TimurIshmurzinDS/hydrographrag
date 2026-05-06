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

   # Hardcoded list of dictionaries containing the coordinates (WKT) from the context
   points = [{'name': 'Карталь River Mouth', 'coordinates': 'POINT (X Y)'}, {'name': '1.1 km above Lake Ulken Almaty', 'coordinates': 'POINT (X Y)'}]

   # Add each point to the map as a folium.Marker
   for point in points:
       coordinates = wkt.loads(point['coordinates'])
       folium.Marker([coordinates.y, coordinates.x], popup=point['name']).add_to(m)

   # Save the final map
   m.save("102.html")