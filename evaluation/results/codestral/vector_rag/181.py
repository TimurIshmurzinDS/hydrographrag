python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the basin data
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Hardcoded list of dictionaries for river features (replace with actual data if available)
       rivers = [{'name': 'Sharyn River', 'water_level': Water_level_Value, 'quality_class': Water_quality_class, 'date': Date_water_level_Value}]

       # Add markers for each river on the map (replace with actual coordinates if available)
       for river in rivers:
           folium.Marker([0, 0], popup=river['name'] + '<br>' + str(river['water_level']) + '<br>' + river['quality_class']).add_to(m)

       # Save the final map
       m.save("181.html")