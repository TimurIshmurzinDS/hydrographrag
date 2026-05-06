python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for the Emel River incident (if coordinates are available)
       incidents = [{'name': 'Emel River Incident', 'location': wkt.loads('POINT (-123.456 78.901)')}]

       # Add markers for each incident to the map
       for incident in incidents:
           folium.Marker(location=[incident['location'].y, incident['location'].x], popup=incident['name']).add_to(m)

       # Save the final map
       m.save("265.html")