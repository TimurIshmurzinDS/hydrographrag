python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize the map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for the observation point (replace with actual data if available)
       points = [{'name': 'Observation Point', 'geometry': wkt.loads('POINT (longitude latitude)')}]

       # Add the observation point to the map
       for point in points:
           folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

       # Save the final map
       m.save("26.html")