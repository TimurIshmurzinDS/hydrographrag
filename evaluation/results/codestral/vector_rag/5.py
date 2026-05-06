python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map with basin centroid
       m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for observations (replace with actual data if available)
       observations = [{'name': 'Observation 1', 'geometry': wkt.loads('POINT (37.654890 55.752220)'},
                       {'name': 'Observation 2', 'geometry': wkt.loads('POINT (37.654890 55.712220)'} ] # Replace with actual coordinates

       # Add observations to the map
       for observation in observations:
           folium.Marker(location=[observation['geometry'].y, observation['geometry'].x], popup=observation['name']).add_to(m)

       # Save the final map
       m.save("5.html")