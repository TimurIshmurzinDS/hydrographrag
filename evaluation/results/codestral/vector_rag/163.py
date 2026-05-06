python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin_data = gpd.read_file(r"data/basin_data.shp")
   basin_data = basin_data.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for rivers (if coordinates are available in the context)
   rivers = [{'name': 'Sarykan River', 'coordinates': None}, {'name': 'Shyzhyn River', 'coordinates': None}]

   # If coordinates are available, create markers on the map
   for river in rivers:
       if river['coordinates'] is not None:
           folium.Marker(location=wkt.loads(river['coordinates']).coords[0][::-1], popup=river['name']).add_to(m)

   # Save the final map
   m.save("163.html")