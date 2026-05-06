python
         import pandas as pd
         import folium
         # Load data
         baskan_data = pd.read_csv('baskan_river_data.csv')
         prokhodnaya_data = pd.read_csv('prokhodnaya_river_data.csv')
         # Check for missing values
         print(baskan_data.isnull().sum())
         print(prokhodnaya_data.isnull().sum())
         # Calculate mean discharge during peak flood period
         baskan_mean = baskan_data['discharge'].mean()
         prokhodnaya_mean = prokhodnaya_data['discharge'].mean()
         # Compare means
         difference = baskan_mean - prokhodnaya_mean
         print(f'The current discharge on Baskan River is {difference} cubic meters per second higher than the level on Prokhodnaya River during peak flood period.')
         # Visualize data on map
         m = folium.Map(location=[55, 37], zoom_start=6)
         folium.Marker([55.12, 40.89], popup='Baskan River').add_to(m)
         folium.Marker([54.98, 41.47], popup='Prokhodnaya River').add_to(m)
         m.save('89.html')