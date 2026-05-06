python
        # Import necessary libraries
        import geopandas as gpd
        import folium

        # Load the data
        rivers = gpd.read_file('path_to_your_data/talgar_river.shp')
        tributaries = gpd.read_file('path_to_your_data/tributaries.shp')

        # Find intersection points between the main river and its tributaries
        intersections = gpd.sjoin(rivers, tributaries, how="inner", op='intersects')

        # Create a folium map centered around the main river
        m = folium.Map(location=[intersections['geometry'].y.mean(), intersections['geometry'].x.mean()], zoom_start=10)

        # Add the main river to the map
        folium.GeoJson(rivers).add_to(m)

        # Add the tributaries to the map
        folium.GeoJson(tributaries).add_to(m)

        # Add the intersection points to the map
        for idx, row in intersections.iterrows():
            folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=5, color='red').add_to(m)

        # Save the map
        m.save("166.html")