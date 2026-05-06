python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize the map with the centroid of the basin
       m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of observation points near Ili River and Ile River (if coordinates are provided)
       observation_points = [{'name': 'Observation near Ili', 'coordinates': wkt.loads('POINT (76.951043 42.822957)'},
                             {'name': 'Observation near Ile', 'coordinates': wkt.loads('POINT (77.051043 42.922957)'}
                            ]

       # Add observation points to the map
       for point in observation_points:
           folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

       # Save the final map
       m.save("1.html")