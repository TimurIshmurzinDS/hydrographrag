python
        import folium
        import geopandas as gpd

        # Load the data (replace 'rivers_data.geojson' with your actual file path)
        rivers = gpd.read_file('rivers_data.geojson')

        # Define normal water levels for each river considering spring thaw
        normal_levels = {
            "Baskan River": 5,   # replace with the actual normal level
            "Prokhodnaya River": 3  # replace with the actual normal level
        }

        # Compare current water levels with normal levels
        rivers['exceed_normal'] = rivers.apply(lambda row: row['water_level'] > normal_levels[row['river_name']], axis=1)

        # Create a map centered around the area of interest
        m = folium.Map(location=[55, 37], zoom_start=6)

        # Add rivers to the map with different colors based on water level comparison
        for _, r in rivers.iterrows():
            color = 'red' if r['exceed_normal'] else 'blue'
            folium.GeoJson(r['geometry'], style_function=lambda x, color=color: {'fillColor': color}).add_to(m)

        # Save the map as an HTML file
        m.save("81.html")