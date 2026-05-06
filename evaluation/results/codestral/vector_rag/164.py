python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin_data = gpd.read_file(r"data/basin_data.shp")
   basin_data = basin_data.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers and observation point (replace with actual data if available)
   features = [{'name': 'Ili River', 'geometry': wkt.loads('POINT(71.8359 51.2046)'},
               {'name': 'Shynzhaly River', 'geometry': wkt.loads('POINT(72.0236 51.7852)'},
               {'name': 'Shyzhyn River', 'geometry': wkt.loads('POINT(74.9877 53.5174)'},
               {'name': 'Byzhy River', 'geometry': wkt.loads('POINT(69.0234 52.2878)'},
               {'name': 'Observation near Ili', 'geometry': wkt.loads('POINT(71.7500 51.2500)'}
              ]

   # Add rivers and observation point to the map
   for feature in features:
       folium.Marker([feature['geometry'].y, feature['geometry'].x], popup=feature['name']).add_to(m)

   # Save the final map
   m.save("164.html")