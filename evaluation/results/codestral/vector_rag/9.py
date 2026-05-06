python
       import geopandas as gpd
       import folium
       from shapely.wkt import loads

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for rivers (replace with actual coordinates if available)
       rivers = [{'name': 'Ili River', 'coordinates': 'POINT(76.153984 42.204102)'},
                 {'name': 'Karatal River', 'coordinates': 'POINT(76.923611 42.358056)'}]

       # Add rivers to the map
       for river in rivers:
           point = loads(river['coordinates'])
           folium.Marker([point.y, point.x], popup=river['name']).add_to(m)

       # Save the final map
       m.save("9.html")