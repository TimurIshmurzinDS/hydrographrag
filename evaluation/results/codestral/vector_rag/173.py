python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for Shynzhaly River coordinates (WKT)
   rivers = [{'name': 'Shynzhaly River', 'coordinates': wkt.loads('POINT (71.4308 51.2096)')}]

   # Add the rivers to the map
   for river in rivers:
       folium.Marker(location=[river['coordinates'].y, river['coordinates'].x], popup=river['name']).add_to(m)

   # Save the final map
   m.save("173.html")