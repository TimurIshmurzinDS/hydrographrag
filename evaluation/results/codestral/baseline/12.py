python
         import geopandas as gpd
         import folium
         from scipy import stats

         # Load sensor data
         sensor_data = gpd.read_file('sensor_data.shp')

         # Create a base map
         m = folium.Map(location=[sensor_data['geometry'].centroid.y.mean(), sensor_data['geometry'].centroid.x.mean()], zoom_start=10)

         # Add sensor data to the map
         for idx, row in sensor_data.iterrows():
             folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], radius=5, color='blue').add_to(m)

         # Detect outliers using Z-score
         z_scores = stats.zscore(sensor_data['sensor_value'])
         outliers = sensor_data[(z_scores > 3) | (z_scores < -3)]

         # Add outliers to the map
         for idx, row in outliers.iterrows():
             folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], radius=10, color='red').add_to(m)

         # Save the final map
         m.save("12.html")