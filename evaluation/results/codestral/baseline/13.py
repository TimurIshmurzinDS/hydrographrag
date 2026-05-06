python
        import folium
        import geopandas as gpd

        # Load data
        data = gpd.read_file('kumbel_river_data.geojson')  # replace with your file path and format

        # Create a map centered around the Kumbel River
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        # Add water level points to the map
        for idx, row in data.iterrows():
            color = 'blue' if row['water_level'] < 5 else 'red'  # adjust threshold as needed
            folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=6, color=color, fill=True, fill_color=color).add_to(m)

        # Save the map
        m.save("13.html")