python
        import geopandas as gpd
        import folium

        # Load the sensor data
        sensors = gpd.read_file('path_to_your_sensor_data')

        # Check if 'status' column exists
        if 'status' not in sensors.columns:
            raise ValueError("The dataset does not contain a 'status' column.")

        # Create a folium map centered around the Kumbel River area
        m = folium.Map(location=[sensors['geometry'].y.mean(), sensors['geometry'].x.mean()], zoom_start=10)

        # Add markers to the map for each sensor, colored based on status
        for _, row in sensors.iterrows():
            if row['status'] == 'normal':
                color = 'green'
            else:
                color = 'red'
            folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], radius=5, color=color).add_to(m)

        # Save the map as an HTML file
        m.save("6.html")