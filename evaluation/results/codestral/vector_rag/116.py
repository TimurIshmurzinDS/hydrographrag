python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with coordinates (WKT) if available in the context
   points = [{'name': 'Tekeli town', 'coordinates': wkt.loads('POINT (37.123456 49.123456)'}, {'name': 'Tekeli River', 'coordinates': wkt.loads('LINESTRING (37.123456 49.123456, 37.234567 49.234567)'), ...]

   # Add points to the map
   for point in points:
       folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

   # Save the final map
   m.save("116.html")