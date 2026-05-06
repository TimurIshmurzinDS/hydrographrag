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

       # Hardcoded list of dictionaries for observations (replace with actual data if available)
       observations = [{'name': 'Observation 1', 'geometry': wkt.loads('POINT (37.618423 55.751244)'},
                       {'name': 'Observation 2', 'geometry': wkt.loads('POINT (37.619000 55.751000)'}
                      ]

       # Add observations to the map
       for observation in observations:
           folium.Marker(location=[observation['geometry'].y, observation['geometry'].x], popup=observation['name']).add_to(m)

       # Save the final map
       m.save("12.html")