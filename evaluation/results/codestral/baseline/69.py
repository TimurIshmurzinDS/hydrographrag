python
        import folium
        import pandas as pd

        # Load data
        koktal_data = pd.read_csv('koktal_sensors.csv')
        aksu_data = pd.read_csv('aksu_sensors.csv')

        # Create map centered around the average coordinates of both rivers
        avg_latitude = (koktal_data['lat'].mean() + aksu_data['lat'].mean()) / 2
        avg_longitude = (koktal_data['lon'].mean() + aksu_data['lon'].mean()) / 2
        m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=10)

        # Define color and icon based on sensor status
        def get_color_and_icon(status):
            if status == 'normal':
                return 'green', 'ok'
            elif status == 'attention':
                return 'red', 'warning'
            else:
                return 'gray', 'remove'

        # Add Koktal River sensors to the map
        for _, row in koktal_data.iterrows():
            color, icon = get_color_and_icon(row['status'])
            folium.Marker([row['lat'], row['lon']], popup=f"Sensor ID: {row['id']}\nStatus: {row['status']}",
                          icon=folium.Icon(color=color, icon=icon)).add_to(m)

        # Add Aksu River sensors to the map
        for _, row in aksu_data.iterrows():
            color, icon = get_color_and_icon(row['status'])
            folium.Marker([row['lat'], row['lon']], popup=f"Sensor ID: {row['id']}\nStatus: {row['status']}",
                          icon=folium.Icon(color=color, icon=icon)).add_to(m)

        # Save the map as HTML file
        m.save("69.html")