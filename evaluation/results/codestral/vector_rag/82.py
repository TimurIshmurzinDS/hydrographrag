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
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries representing the posts on Karaoy River with their water consumption values
   posts = [{'name': 'Post1', 'coordinates': wkt.loads('POINT (37.6200 55.7540)'), 'water_consumption': 50},
            {'name': 'Post2', 'coordinates': wkt.loads('POINT (37.6300 55.7550)'), 'water_consumption': 60}]

   # Define the critical water consumption level for floods
   CRITICAL_LEVEL = 100

   # Add posts to the map and check their water consumption levels
   for post in posts:
       if post['water_consumption'] > CRITICAL_LEVEL:
           color = 'red'
       else:
           color = 'blue'
       folium.Marker(location=[post['coordinates'].y, post['coordinates'].x], popup=post['name'], icon=folium.Icon(color=color)).add_to(m)

   # Save the final map
   m.save("82.html")