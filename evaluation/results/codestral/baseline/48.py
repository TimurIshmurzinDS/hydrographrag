python
         import pandas as pd
         import geopandas as gpd
         import folium
         # Load historical water consumption data for Karkara River from 2010 to 2020
         water_data = pd.read_csv('water_consumption.csv')
         # Load geographic data for Karkara River
         river_data = gpd.read_file('river_geometry.shp')
         # Merge water consumption data with river geometry data
         merged_data = pd.merge(water_data, river_data, on='river_id')
         # Create a folium map object
         m = folium.Map(location=[merged_data['lat'].mean(), merged_data['lon'].mean()], zoom_start=10)
         # Add a layer for the river geometry
         folium.GeoJson(river_data).add_to(m)
         # Add a layer for water consumption data
         folium.Choropleth(geo_data=merged_data, data=merged_data, columns=['river_id', 'water_consumption'], key_on='feature.properties.river_id').add_to(m)
         # Save the map to a file
         m.save('48.html')