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

   # Hardcoded list of dictionaries with WKT coordinates (replace with actual data if available)
   features = [{'name': 'Emel River Water Level', 'coordinates': 'POINT(37.6184 55.7512)'},
               {'name': 'Kumbel River Water Level', 'coordinates': 'POINT(39.7204 47.2314)'},
               {'name': 'Bayankol River Water Level', 'coordinates': 'POINT(86.1584 53.3520)'}]

   # Add features to the map
   for feature in features:
       point = loads(feature['coordinates'])
       folium.Marker([point.y, point.x], popup=feature['name']).add_to(m)

   # Save the final map
   m.save("258.html")