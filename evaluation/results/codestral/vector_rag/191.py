python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for observation points (if available in the context)
   observations = [{'name': 'Observation_2264', 'geometry': wkt.loads('POINT (...)')},
                  {'name': 'Observation_2278', 'geometry': wkt.loads('POINT (...)')}]

   # Add observation points to the map (if available)
   for obs in observations:
       folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

   # Save the final map
   m.save("191.html")