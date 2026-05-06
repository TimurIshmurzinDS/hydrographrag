python
         import geopandas as gpd
         import folium
         from shapely.geometry import Point
         from datetime import timedelta

         # Load data
         lepsa_data = gpd.read_file('lepsa_sensor_data.geojson')
         kishosek_data = gpd.read_file('kishosek_sensor_data.geojson')

         # Check for missing signals
         def find_signal_gaps(data):
             data['timestamp'] = pd.to_datetime(data['timestamp'])
             data = data.sort_values('timestamp')
             data['time_diff'] = data['timestamp'].diff()
             gaps = data[data['time_diff'] > timedelta(minutes=15)]  # Assuming a signal every 15 minutes
             return gaps

         lepsa_gaps = find_signal_gaps(lepsa_data)
         kishosek_gaps = find_signal_gaps(kishosek_data)

         # Visualize on map
         m = folium.Map(location=[55, 37], zoom_start=6)

         for idx, row in lepsa_gaps.iterrows():
             folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=5, color='red').add_to(m)

         for idx, row in kishosek_gaps.iterrows():
             folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=5, color='blue').add_to(m)

         m.save("149.html")