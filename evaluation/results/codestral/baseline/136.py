python
        import pandas as pd
        import folium

        # Load data
        data = pd.read_csv('water_level_sensors.csv')

        # Check status of each sensor
        def check_status(row):
            if row['last_data'] > '2022-01-01':  # Assuming 'last_data' is the column with last data timestamp
                return 'Active'
            else:
                return 'Inactive'
        data['status'] = data.apply(check_status, axis=1)

        # Create map
        m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10)

        # Add markers to the map
        for i in range(len(data)):
            if data.iloc[i]['status'] == 'Active':
                color = 'green'
            else:
                color = 'red'
            folium.Marker([data.iloc[i]['lat'], data.iloc[i]['lon']], icon=folium.Icon(color=color)).add_to(m)

        # Save the map
        m.save("136.html")