python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for the rivers and observation point (replace with actual coordinates if available)
   points = [{'name': 'Lepsy River', 'coordinates': wkt.loads('POINT (0 0)')},
              {'name': 'Sarykan River', 'coordinates': wkt.loads('POINT (0 0)')},
              {'name': 'Below the mouth of Sarysai River', 'coordinates': wkt.loads('POINT (0 0)')}]

   # Add the rivers and observation point to the map
   for point in points:
       folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

   # Save the final map
   m.save("113.html")