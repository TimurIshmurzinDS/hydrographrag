python
        import folium
        import pandas as pd

        # Load sensor data into a DataFrame
        sensor_data = pd.read_csv('sensor_data.csv')

        # Create a base map centered around the Osek River
        m = folium.Map(location=[55.794, 49.106], zoom_start=12)

        # Add markers for each sensor on the map
        for i in range(len(sensor_data)):
            if sensor_data.iloc[i]['status'] == 'working':
                color = 'green'
            else:
                color = 'red'
            folium.CircleMarker(location=[sensor_data.iloc[i]['latitude'], sensor_data.iloc[i]['longitude']],
                                radius=5,
                                color=color,
                                fill=True,
                                fill_color=color).add_to(m)

        # Save the map as "68.html"
        m.save("68.html")