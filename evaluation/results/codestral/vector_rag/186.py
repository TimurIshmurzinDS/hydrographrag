python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # If the context contains Coordinates (WKT), create a hardcoded list of dictionaries for Butak village and river
   entities = [
       {'name': 'Butak River', 'type': 'HY_HydroFeature', 'geometry': wkt.loads('POINT(longitude latitude)')},  # Replace longitude and latitude with actual coordinates
       {'name': 'Butak Village', 'type': 'Observation', 'geometry': wkt.loads('POINT(longitude latitude)')}   # Replace longitude and latitude with actual coordinates
   ]

   # Add entities to the map
   for entity in entities:
       folium.Marker([entity['geometry'].y, entity['geometry'].x], popup=entity['name']).add_to(m)

   # Save the final map
   m.save("186.html")