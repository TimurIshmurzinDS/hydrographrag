python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile and convert to CRS 'EPSG:4326'
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map using folium.GeoJson
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for points of interest (water level and consumption)
       points_of_interest = [
           {'location': wkt.loads('POINT (longitude1 latitude1)'), 'type': 'Water Level', 'value': 'Date_water_level_Value'},
           {'location': wkt.loads('POINT (longitude2 latitude2)'), 'type': 'Water Consumption', 'value': 'Water_consumption_Value'}
       ]

       # Add points of interest to the map
       for point in points_of_interest:
           folium.Marker(location=[point['location'].y, point['location'].x], popup=f"{point['type']}: {point['value']}").add_to(m)

       # Save the final map
       m.save("251.html")