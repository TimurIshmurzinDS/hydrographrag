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

   # Hardcoded list of dictionaries for hydro posts on Karaoy River with their water consumption values
   hydro_posts = [
       {"name": "Hydro Post 1", "water_consumption": 50, "coordinates": "POINT (37.6200 55.7536)"},
       {"name": "Hydro Post 2", "water_consumption": 45, "coordinates": "POINT (37.6189 55.7520)"},
       # Add more hydro posts as needed
   ]

   # Convert WKT coordinates to Shapely Point objects and add them to the map
   for post in hydro_posts:
       point = wkt.loads(post["coordinates"])
       folium.Marker([point.y, point.x], popup=f"{post['name']}: {post['water_consumption']} m³/s").add_to(m)

   # Save the final map
   m.save("76.html")