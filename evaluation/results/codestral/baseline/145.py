python
        import folium
        import pandas as pd
        from sqlalchemy import create_engine

        # Connect to the database
        engine = create_engine('your_database_connection_string')

        # Query data from the database
        query = "SELECT latitude, longitude, status, sensor_id FROM sensors WHERE river IS NOT NULL"
        df = pd.read_sql(query, engine)

        # Create a map centered around the average location of all sensors
        avg_lat = df['latitude'].mean()
        avg_lon = df['longitude'].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

        # Define color and icon for each sensor status
        def get_color(status):
            if status == 'Working':
                return 'green'
            else:
                return 'red'

        def get_icon(status):
            if status == 'Working':
                return 'check'
            else:
                return 'remove'

        # Add markers to the map for each sensor
        for index, row in df.iterrows():
            folium.Marker([row['latitude'], row['longitude']],
                           popup=f"Sensor ID: {row['sensor_id']}<br>Status: {row['status']}",
                           icon=folium.Icon(color=get_color(row['status']), icon=get_icon(row['status']))).add_to(m)

        # Save the map as an HTML file
        m.save("145.html")