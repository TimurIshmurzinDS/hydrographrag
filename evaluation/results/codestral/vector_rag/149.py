python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Assuming we have a DataFrame df containing water level data with columns 'Observation', 'Date_water_level_Value' and 'Water_level_Value'
   # We need to find gaps in the observations for rivers Lepsy and Kish Osek

   # Filter data for Lepsy and Kish Osek rivers
   lepsy_data = df[df['River'] == 'Lepsy']
   kish_osek_data = df[df['River'] == 'Kish Osek']

   # Find gaps in observations
   def find_gaps(data):
       data = data.sort_values('Date_water_level_Value')
       data['Time_diff'] = data['Date_water_level_Value'].diff()
       gaps = data[data['Time_diff'] > pd.Timedelta(days=1)]
       return gaps

   lepsy_gaps = find_gaps(lepsy_data)
   kish_osek_gaps = find_gaps(kish_osek_data)

   # Print the gaps
   print("Gaps in Lepsy observations:")
   print(lepsy_gaps)
   print("\nGaps in Kish Osek observations:")
   print(kish_osek_gaps)

   # Save the final map
   m.save("149.html")