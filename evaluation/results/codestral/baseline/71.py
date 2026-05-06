python
         import folium
         import geopandas as gpd
         # Load sensor data
         sensors = gpd.read_file('sensors_data.geojson')
         # Check if the 'status' attribute exists, otherwise request status from the sensor management system
         if 'status' not in sensors.columns:
             # Code to request sensor status goes here
             pass
         # Filter active sensors
         active_sensors = sensors[sensors['status'] == 'active']
         # Create a map centered around Byzhy River
         m = folium.Map(location=[53.9024, 37.6178], zoom_start=12)
         # Add active sensors to the map
         for idx, row in active_sensors.iterrows():
             folium.Marker([row['geometry'].y, row['geometry'].x]).add_to(m)
         # Save the map as an HTML file
         m.save("71.html")