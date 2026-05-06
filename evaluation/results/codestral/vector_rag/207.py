python
   import pandas as pd
   import geopandas as gpd
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Hardcoded list of dictionaries for the observation point (replace with actual data)
   points = [{'name': 'Observation Point', 'geometry': wkt.loads('POINT(longitude latitude)')}]

   # Load water level data for Emel River and Turgen River (replace with actual data)
   emel_data = pd.read_csv('emel_river_water_levels.csv')
   turgen_data = pd.read_csv('turgen_river_water_levels.csv')

   # Define a function to count extreme low flows (replace with actual threshold)
   def count_extreme_low_flows(data):
       return sum(data['water_level'] < threshold)

   # Count extreme low flows for Emel River and Turgen River
   emel_extreme_count = count_extreme_low_flows(emel_data)
   turgen_extreme_count = count_extreme_low_flows(turgen_data)

   # Compare the results and print the analysis
   if emel_extreme_count > turgen_extreme_count:
       print("The Emel River has experienced more extreme low flows than the Turgen River over the last two decades.")
   elif emel_extreme_count < turgen_extreme_count:
       print("The Turgen River has experienced more extreme low flows than the Emel River over the last two decades.")
   else:
       print("Both rivers have experienced an equal number of extreme low flows over the last two decades.")