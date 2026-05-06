python
         import pandas as pd
         import folium
         from shapely.geometry import Point

         # Load sensor data
         tokyr_data = pd.read_csv('tokyr_sensor_data.csv')
         ayagoz_data = pd.read_csv('ayagoz_sensor_data.csv')

         # Define time interval for analysis
         start_date = '2021-01-01'
         end_date = '2021-12-31'

         # Filter data within the defined time interval
         tokyr_data = tokyr_data[(tokyr_data['timestamp'] >= start_date) & (tokyr_data['timestamp'] <= end_date)]
         ayagoz_data = ayagoz_data[(ayagoz_data['timestamp'] >= start_date) & (ayagoz_data['timestamp'] <= end_date)]

         # Calculate data loss percentage for each sensor
         def calculate_data_loss(df):
             total_records = len(df)
             lost_records = df[df['data'].isnull()].shape[0]
             return (lost_records / total_records) * 100

         tokyr_data['data_loss'] = calculate_data_loss(tokyr_data)
         ayagoz_data['data_loss'] = calculate_data_loss(ayagoz_data)

         # Create a map centered around the region of interest
         m = folium.Map(location=[51.0, 71.0], zoom_start=6)

         # Add markers for each sensor on the map with data loss percentage as popup
         for index, row in tokyr_data.iterrows():
             folium.Marker([row['latitude'], row['longitude']],
                           popup='Tokyr Sensor\nData Loss: {:.2f}%'.format(row['data_loss'])).add_to(m)

         for index, row in ayagoz_data.iterrows():
             folium.Marker([row['latitude'], row['longitude']],
                           popup='Ayagoz Sensor\nData Loss: {:.2f}%'.format(row['data_loss'])).add_to(m)

         # Save the map as HTML file
         m.save("140.html")