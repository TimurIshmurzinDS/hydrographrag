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

       # Hardcoded list of observations with coordinates and water levels
       observations = [
           {"coordinates": "POINT (37.618490 55.751244)", "water_level": 10.5},
           {"coordinates": "POINT (37.620000 55.750000)", "water_level": 11.2}
       ]

       # Add observations to the map
       for obs in observations:
           coords = wkt.loads(obs['coordinates'])
           folium.Marker([coords.y, coords.x], popup=f"Water level: {obs['water_level']} m").add_to(m)

       # Save the final map
       m.save("67.html")