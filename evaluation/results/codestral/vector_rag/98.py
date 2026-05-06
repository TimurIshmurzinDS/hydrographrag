python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basins = gpd.read_file(r"data/basin_data.shp")
       basins = basins.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basins['geometry'].centroid.y.mean(), basins['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Add basins to the map
       folium.GeoJson(basins, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of rivers with their coordinates (WKT format)
       rivers = [
           {"name": "Tentek River", "coordinates": "POINT(longitude latitude)"},
           {"name": "Byzhy River", "coordinates": "POINT(longitude latitude)"}
       ]

       # Check in which basin the rivers fall into
       for river in rivers:
           point = wkt.loads(river['coordinates'])
           for idx, row in basins.iterrows():
               if row['geometry'].contains(point):
                   print(f"{river['name']} falls into {row['Basin_Name']}")

       # Save the final map
       m.save("98.html")