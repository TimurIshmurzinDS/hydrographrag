python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin_data = gpd.read_file(r"data/basin_data.shp")
       basin_data = basin_data.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for the rivers' coordinates (WKT)
       rivers = [{'name': 'Emel River', 'coordinates': wkt.loads('POINT (longitude1 latitude1)')},
                 {'name': 'Sarykan River', 'coordinates': wkt.loads('POINT (longitude2 latitude2)')}]

       # Add the rivers to the map
       for river in rivers:
           folium.Marker(location=[river['coordinates'].y, river['coordinates'].x], popup=river['name']).add_to(m)

       # Save the final map
       m.save("168.html")