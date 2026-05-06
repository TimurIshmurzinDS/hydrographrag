python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries for water level data (replace with actual data)
   water_level_data = [{'Water_level_Value': 10, 'Date_water_level_Value': '2022-01-01'},
                       {'Water_level_Value': 12, 'Date_water_level_Value': '2022-01-02'}]
   water_level_df = pd.DataFrame(water_level_data)

   # Convert date strings to datetime objects
   water_level_df['Date_water_level_Value'] = pd.to_datetime(water_level_df['Date_water_level_Value'])

   # Plot the water level data on the map (replace with actual coordinates)
   for i, row in water_level_df.iterrows():
       folium.CircleMarker(location=[55.751244, 37.618423], radius=row['Water_level_Value'], color='blue', fill=True, fill_color='blue').add_to(m)

   # Save the final map
   m.save("14.html")