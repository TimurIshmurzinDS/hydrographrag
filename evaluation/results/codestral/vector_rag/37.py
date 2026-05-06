python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd

   # Load the data (assuming it's in a CSV file)
   data = pd.read_csv('data/river_data.csv')

   # Calculate statistics
   average_consumption = data['Water_consumption_Valuem³s'].mean()
   max_consumption = data['Water_consumption_Valuem³s'].max()
   min_consumption = data['Water_consumption_Valuem³s'].min()

   # Seasonal analysis (assuming 'Date' column is in datetime format)
   data['Month'] = data['Date'].dt.month
   seasonal_analysis = data.groupby('Month')['Water_consumption_Valuem³s'].mean()

   print(f"Average water consumption: {average_consumption} m³")
   print(f"Maximum water consumption: {max_consumption} m³")
   print(f"Minimum water consumption: {min_consumption} m³")
   print("Seasonal analysis of water consumption:\n", seasonal_analysis)