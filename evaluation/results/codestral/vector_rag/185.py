python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd
   from scipy import stats

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Load water consumption data and crop yield data (assuming they are in CSV format)
   water_consumption = pd.read_csv('water_consumption_data.csv')
   crop_yield = pd.read_csv('crop_yield_data.csv')

   # Merge the two datasets based on time period
   data = pd.merge(water_consumption, crop_yield, on='time_period')

   # Calculate correlation between water consumption and crop yield
   correlation, p_value = stats.pearsonr(data['Water_consumption_Value'], data['Crop_Yield'])

   print(f'The correlation coefficient is {correlation} with a p-value of {p_value}.')

   # Save the final map
   m.save("185.html")