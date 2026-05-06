python
   import geopandas as gpd
   import folium
   from shapely import wkt
   from datetime import datetime

   # Load the shapefile
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Assuming we have a DataFrame df with columns 'River', 'Date_water_level_Value'
   byzhy_river_data = df[df['River'] == 'Byzhy River']
   last_update = byzhy_river_data['Date_water_level_Value'].max()

   # Check if the sensor is active (assuming a threshold of 7 days)
   if (datetime.now() - last_update).days <= 7:
       print("The sensors on Byzhy River are in active mode.")
   else:
       print("The sensors on Byzhy River are not in active mode.")

   # Save the final map
   m.save("71.html")