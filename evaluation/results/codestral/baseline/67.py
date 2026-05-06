python
        import folium
        import pandas as pd

        # Load data
        data = pd.read_csv('prokhodnaya_river_data.csv')

        # Create map centered at the mean coordinates of the river posts
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        # Add markers to the map for each post, displaying the last recorded water level
        for i in range(len(data)):
            folium.Marker([data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                          popup=f"Post: {data.iloc[i]['post_name']}<br>Last Water Level: {data.iloc[i]['last_water_level']}").add_to(m)

        # Save the map as 67.html
        m.save("67.html")