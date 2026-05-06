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
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for the observation point
   observations = [{'name': '1.7 km above Kishi Osek River', 'wkt': 'POINT (longitude latitude)'}]

   # Add the observation points to the map
   for obs in observations:
       folium.GeoJson(wkt.loads(obs['wkt']), tooltip=obs['name'], icon=folium.Icon(color='red')).add_to(m)

   # Save the final map
   m.save("179.html")