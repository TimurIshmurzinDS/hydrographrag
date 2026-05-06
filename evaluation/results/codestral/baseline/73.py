python
         import folium
         import pandas as pd
         # Assuming we have a DataFrame df with columns 'river', 'sensor_id', 'location', and 'status'
         # Load data into a Pandas DataFrame
         df = pd.read_csv('water_level_sensors.csv')
         # Filter data for Osek River and Koktal River
         osek_data = df[df['river'] == 'Osek River']
         koktal_data = df[df['river'] == 'Koktal River']
         # Create a base map centered around the area of interest
         m = folium.Map(location=[55, 60], zoom_start=8)
         # Define color mapping for sensor status
         colors = {'Normal': 'green', 'Warning': 'orange', 'Critical': 'red'}
         # Add markers to the map for each sensor on Osek River
         for i, row in osek_data.iterrows():
             folium.CircleMarker(location=row['location'], radius=10, color=colors[row['status']], fill=True).add_to(m)
         # Add markers to the map for each sensor on Koktal River
         for i, row in koktal_data.iterrows():
             folium.CircleMarker(location=row['location'], radius=10, color=colors[row['status']], fill=True).add_to(m)
         # Save the map as an HTML file
         m.save("73.html")