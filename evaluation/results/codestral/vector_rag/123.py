python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map using the centroid of the shapefile
       m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for rivers (replace with actual data if available)
       rivers = [{'name': 'Kurty River', 'wkt': 'LINESTRING(...)'},
                 {'name': 'Sharyn River', 'wkt': 'LINESTRING(...)'},
                 # Add other rivers here...
                ]

       # Add rivers to the map
       for river in rivers:
           folium.GeoJson(data=wkt.loads(river['wkt']), style_function=lambda x: {'color': 'blue'}).add_to(m)

       # Save the final map
       m.save("123.html")