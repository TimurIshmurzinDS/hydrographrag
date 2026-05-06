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

   # Hardcoded list of dictionaries for river coordinates (WKT)
   rivers = [{'name': 'Sharyn River', 'coordinates': wkt.loads('POINT (69.583741 50.265000)'},
             {'name': 'Uzyn Kargaly River', 'coordinates': wkt.loads('POINT (70.006000 49.999722)'}
            ]

   # Add rivers to the map
   for river in rivers:
       folium.Marker(location=[river['coordinates'].y, river['coordinates'].x], popup=river['name']).add_to(m)

   # Save the final map
   m.save("234.html")