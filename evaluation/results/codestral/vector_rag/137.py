python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Load the shapefile
       basins = gpd.read_file(r"data/basin_data.shp")
       basins = basins.to_crs('EPSG:4326')

       # Initialize folium map
       m = folium.Map(location=[basins['geometry'].centroid.y.mean(), basins['geometry'].centroid.x.mean()], tiles='CartoDB positron', zoom_start=10)

       # Add the basin to the map
       folium.GeoJson(basins, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

       # Save the final map
       m.save("137.html")