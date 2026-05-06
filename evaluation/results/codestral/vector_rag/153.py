python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize the map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for the mouth of Sarysai River (replace with actual coordinates if available)
   observations = [{'name': 'below the mouth of Sarysai River', 'geometry': wkt.loads('POINT (0 0)')}]

   # Convert to GeoDataFrame and add to map
   gdf_observations = gpd.GeoDataFrame(observations, geometry='geometry')
   folium.GeoJson(gdf_observations['geometry'], name='Observations', style_function=lambda x: {'color': 'red'}).add_to(m)

   # Save the final map
   m.save("153.html")