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

   # Assuming we have a list of dictionaries containing water level data and coordinates in WKT format
   water_level_data = [
       {'coordinates': 'POINT (37.618423 55.751244)', 'water_level': 100, 'date': '2022-01-01'},
       # Add more data as needed
   ]

   # Add water level data to the map
   for data in water_level_data:
       folium.CircleMarker(location=wkt.loads(data['coordinates']).coords[0], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)

   # Save the final map
   m.save("145.html")