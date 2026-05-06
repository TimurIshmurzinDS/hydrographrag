python
        # Import necessary libraries
        import pandas as pd
        import folium
        from folium.plugins import HeatMap

        # Load the data
        water_data = pd.read_csv('karatal_river_water_consumption.csv')

        # Analyze the data to find optimal collection period
        water_data['rolling_mean'] = water_data['water_consumption'].rolling(window=7).mean()
        optimal_period = water_data[water_data['rolling_mean'] == water_data['rolling_mean'].max()]

        # Load the data about sources of water in Karatal River
        sources_data = pd.read_csv('karatal_river_sources.csv')

        # Create a map centered around Karatal River
        m = folium.Map(location=[sources_data['latitude'].mean(), sources_data['longitude'].mean()], zoom_start=10)

        # Add heatmap of water consumption to the map
        HeatMap(data=water_data[['latitude', 'longitude', 'water_consumption']].values.tolist()).add_to(m)

        # Add markers for sources of water to the map
        for index, row in sources_data.iterrows():
            folium.Marker([row['latitude'], row['longitude']], popup=f'Source {index+1}').add_to(m)

        # Highlight optimal collection period on the map
        for index, row in optimal_period.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=10, color='red', fill=True, fill_color='red').add_to(m)

        # Save the map
        m.save("214.html")