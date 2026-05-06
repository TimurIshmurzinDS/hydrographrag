python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries with water level data (replace this with actual data)
       water_level_data = [{'Date_water_level_Value': 'YYYY-MM-DD', 'Water_level_Value': value}]

       # Add water level data to the map as markers
       for data in water_level_data:
           folium.Marker(location=[0, 0], popup=f"Date: {data['Date_water_level_Value']}, Water Level: {data['Water_level_Value']}").add_to(m)

       # Save the final map
       m.save("144.html")