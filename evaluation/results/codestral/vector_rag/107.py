python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries with river and village coordinates (WKT)
   entities = [
       {"name": "Tekeli River", "coordinates": "POINT(...)"},
       {"name": "Temirlik River", "coordinates": "POINT(...)"},
       {"name": "Temirlik village", "coordinates": "POINT(...)"}
   ]

   # Add rivers and village to the map
   for entity in entities:
       folium.Marker(location=wkt.loads(entity["coordinates"]).coords[0], popup=entity["name"]).add_to(m)

   # Save the final map
   m.save("107.html")