python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for points (replace with actual data if available)
       points = [{'name': 'Urzhar River - 2 km above mouth of Prokhodnoy River', 'wkt': None},
                 {'name': 'Urzhar River - 0.2 km above the confluence with Osek River', 'wkt': None}]

       # If WKT coordinates are available, add points to map and calculate distance
       for point in points:
           if point['wkt'] is not None:
               geometry = wkt.loads(point['wkt'])
               folium.Marker([geometry.y, geometry.x], popup=point['name']).add_to(m)

       # Save the final map
       m.save("96.html")