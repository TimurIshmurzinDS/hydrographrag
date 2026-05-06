python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize the map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for observation points (replace with actual data if available)
   observations = [{'name': 'Observation at Baskan River', 'coordinates': wkt.loads('POINT (37.618423 55.751244)'},
                   {'name': 'Observation near Prokhodnaya River mouth', 'coordinates': wkt.loads('POINT (37.609869 55.744521)'}
                  ]

   # Add observation points to the map
   for obs in observations:
       folium.Marker(location=[obs['coordinates'].y, obs['coordinates'].x], popup=obs['name']).add_to(m)

   # Save the final map
   m.save("89.html")