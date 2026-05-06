python
        import folium
        from folium.plugins import MarkerCluster
        import geopandas as gpd
        from datetime import datetime, timedelta

        # Load the data
        monitoring_posts = gpd.read_file('monitoring_posts.geojson')

        # Check which posts are not transmitting data
        # Assuming that 'last_update' column contains the date and time of last data transmission
        one_day_ago = datetime.now() - timedelta(days=1)
        non_transmitting_posts = monitoring_posts[monitoring_posts['last_update'] < one_day_ago]

        # Create a map centered around the Sharyn River
        m = folium.Map(location=[56, 70], zoom_start=6)

        # Add markers for non-transmitting posts to the map
        marker_cluster = MarkerCluster().add_to(m)
        for idx, row in non_transmitting_posts.iterrows():
            folium.Marker([row['geometry'].y, row['geometry'].x],
                           popup='Post ID: ' + str(row['post_id']),
                           icon=folium.Icon(color="red", icon="warning-sign")).add_to(marker_cluster)

        # Save the map
        m.save("62.html")