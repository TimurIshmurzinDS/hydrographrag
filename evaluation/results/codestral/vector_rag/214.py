python
   import geopandas as gpd
   import folium
   from shapely.geometry import Point

   # Load the shapefile
   basin_data = gpd.read_file(r"data/basin_data.shp")
   basin_data = basin_data.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin_data.__geo_interface__, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Save the final map
   m.save("214.html")