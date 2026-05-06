python
        import folium
        import pandas as pd

        # Load data (assuming it's in CSV format)
        data = pd.read_csv('sensor_data.csv')

        # Create a map centered around Talgar River
        m = folium.Map(location=[42.315, 71.906], zoom_start=10)

        # Define color and icon based on sensor status
        def get_color(status):
            if status == 'normal':
                return 'green'
            elif status == 'attention':
                return 'red'

        def get_icon(status):
            if status == 'normal':
                return 'ok-sign'
            elif status == 'attention':
                return 'exclamation-sign'

        # Add markers to the map for each sensor
        for index, row in data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Sensor ID: {row['sensor_id']}<br>Status: {row['status']}",
                icon=folium.Icon(color=get_color(row['status']), icon=get_icon(row['status']))
            ).add_to(m)

        # Save the map as HTML file
        m.save("10.html")