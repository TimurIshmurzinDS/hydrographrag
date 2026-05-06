python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
   # For example, if we have coordinates for the river's source and mouth
   coordinates = [{'location': wkt.loads('POINT (69.7201 39.8579)'), 'popup': 'Source'}, {'location': wkt.loads('POINT (69.4792 39.6270)'), 'popup': 'Mouth'}]

   # Add the coordinates to the map
   for coord in coordinates:
       folium.Marker(location=[coord['location'].y, coord['location'].x], popup=coord['popup']).add_to(m)

   # Save the final map
   m.save("243.html")