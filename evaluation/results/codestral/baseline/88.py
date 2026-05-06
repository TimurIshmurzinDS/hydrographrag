python
        import geopandas as gpd
        import folium

        # Load data
        river_data = gpd.read_file('koktal_river_data.geojson')

        # Create map centered around the river
        m = folium.Map(location=[river_data['geometry'].centroid.y.mean(), river_data['geometry'].centroid.x.mean()], zoom_start=10)

        # Add river layer to the map
        folium.GeoJson(river_data).add_to(m)

        # Define a function to determine marker color based on water level
        def get_color(water_level):
            if water_level > 5:
                return 'red'
            elif water_level > 3:
                return 'yellow'
            else:
                return 'green'

        # Add markers for each post with popups showing the current water level
        for idx, row in river_data.iterrows():
            folium.CircleMarker(location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
                                radius=5,
                                color=get_color(row['water_level']),
                                fill=True,
                                fill_color=get_color(row['water_level']),
                                popup='Water level: {}'.format(row['water_level'])).add_to(m)

        # Save the map as an HTML file
        m.save("88.html")