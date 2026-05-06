python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map using the centroid of the shapefile
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing river names and coordinates (WKT)
   rivers = [
       {"name": "Kurty River", "coordinates": "POINT (69.457831 50.270769)"},
       {"name": "Urzhar River", "coordinates": "POINT (69.612345 50.123456)"}
   ]

   # Add rivers to the map with markers
   for river in rivers:
       coords = wkt.loads(river["coordinates"]).coords[0]
       folium.Marker(location=[coords[1], coords[0]], popup=river["name"]).add_to(m)

   # Save the final map
   m.save("108.html")