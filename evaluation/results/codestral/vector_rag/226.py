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

   # Hardcoded list of dictionaries for Dobyn pier observations (replace with actual data)
   observations = [{'name': 'Dobyn pier 1', 'coordinates': 'POINT (55.7340 37.6428)', 'water_level': 10},
                   {'name': 'Dobyn pier 2', 'coordinates': 'POINT (55.7350 37.6438)', 'water_level': 12}]

   # Add observations to the map
   for observation in observations:
       folium.Marker(location=[wkt.loads(observation['coordinates']).y, wkt.loads(observation['coordinates']).x],
                     popup=f"{observation['name']}: Water level - {observation['water_level']} m").add_to(m)

   # Save the map
   m.save("226.html")