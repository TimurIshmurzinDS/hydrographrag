python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin_data = gpd.read_file(r"data/basin_data.shp")
       basin_data = basin_data.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin_data['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for village and river coordinates (if available in the context)
       locations = [{'name': 'Tauturgen village', 'coordinates': 'POINT(69.18357 42.40992)', 'type': 'Observation'},
                    {'name': 'Turgen River', 'coordinates': 'LINESTRING(69.18357 42.40992, ...)', 'type': 'HY_HydroFeature'}]

       # Add village and river to the map (if coordinates are available)
       for location in locations:
           if location['coordinates']:
               point = wkt.loads(location['coordinates'])
               folium.Marker([point.y, point.x], popup=location['name'], icon=folium.Icon(color='red' if location['type'] == 'HY_HydroFeature' else 'blue')).add_to(m)

       # Save the final map
       m.save("183.html")