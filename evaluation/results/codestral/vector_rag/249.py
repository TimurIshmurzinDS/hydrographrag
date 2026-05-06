python
   import geopandas as gpd
   import folium
   from shapely.geometry import Point
   from geopy.distance import great_circle

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with coordinates (WKT)
   locations = [{'name': 'г. Talgar', 'coordinates': Point('WKT_COORDINATES')}, {'name': 'Юпитер', 'coordinates': Point('WKT_COORDINATES')}]

   # Calculate distance between Talgar city and Jupiter
   distance = great_circle(locations[0]['coordinates'].coords[0], locations[1]['coordinates'].coords[0]).kilometers

   print(f"The distance between Talgar city and Jupiter is {distance} kilometers.")

   # Save the final map
   m.save("249.html")