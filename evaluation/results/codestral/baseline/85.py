python
        # Import necessary libraries
        import pandas as pd
        import folium
        from folium.plugins import MarkerCluster

        # Load data (assuming CSV format with columns 'Date', 'Koktal_River', 'Baskan_River')
        data = pd.read_csv('river_flow_data.csv')

        # Convert Date column to datetime type
        data['Date'] = pd.to_datetime(data['Date'])

        # Set Date as index
        data.set_index('Date', inplace=True)

        # Define critical flow levels for flood risk (example values, replace with actual data)
        koktal_critical_level = 1000
        baskan_critical_level = 800

        # Create new columns to indicate flood risk based on critical levels
        data['Koktal_Risk'] = data['Koktal_River'].apply(lambda x: 'High' if x > koktal_critical_level else 'Low')
        data['Baskan_Risk'] = data['Baskan_River'].apply(lambda x: 'High' if x > baskan_critical_level else 'Low')

        # For visualization, we need coordinates of the rivers. Replace with actual data.
        koktal_coordinates = [55.012345, 61.298765]
        baskan_coordinates = [54.987654, 61.345678]

        # Create a map centered around the area of interest
        m = folium.Map(location=[55.000000, 61.320000], zoom_start=10)

        # Add markers for each river with popups showing flood risk information
        folium.Marker(koktal_coordinates, popup='Koktal River: {}'.format(data['Koktal_Risk'].iloc[-1])).add_to(m)
        folium.Marker(baskan_coordinates, popup='Baskan River: {}'.format(data['Baskan_Risk'].iloc[-1])).add_to(m)

        # Save the map as an HTML file
        m.save("85.html")