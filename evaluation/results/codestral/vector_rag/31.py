python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile
       basin = gpd.read_file(r"data/basin_data.shp")
       basin = basin.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

       # Add the basin to the map
       folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # If we had data about water consumption, we could add it to the map here
       # For example, if 'Water_consumption_Value' was a column in our basin GeoDataFrame, we could use it to color the basin polygon

       # Save the final map
       m.save("31.html")