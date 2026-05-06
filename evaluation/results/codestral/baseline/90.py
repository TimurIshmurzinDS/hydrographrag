python
        import geopandas as gpd
        import folium

        # Load rivers data
        rivers = gpd.read_file('rivers.geojson')

        # Filter rivers to include only those in the list
        rivers = rivers[rivers['name'].isin(['Karaoy River', 'Baskan River', 'Temirlik River'])]

        # Load flood risk data (assuming it's a GeoJSON file with a 'risk_level' field)
        flood_risk = gpd.read_file('flood_risk.geojson')

        # Join rivers and flood risk data on the river name or ID
        merged = rivers.merge(flood_risk, left_on='name', right_on='river_name')

        # Create a folium map centered around the area of interest
        m = folium.Map(location=[merged['geometry'].centroid.y.mean(), merged['geometry'].centroid.x.mean()], zoom_start=10)

        # Define color scheme for flood risk levels
        def color_producer(risk_level):
            if risk_level == 'low':
                return 'green'
            elif risk_level == 'medium':
                return 'yellow'
            else:
                return 'red'

        # Add rivers to the map with different colors based on flood risk level
        for _, r in merged.iterrows():
            folium.GeoJson(r['geometry'], style_function=lambda x, color=color_producer(r['risk_level']): {'fillColor': color}).add_to(m)

        # Save the map to an HTML file
        m.save("90.html")