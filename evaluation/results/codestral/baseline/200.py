python
        import pandas as pd
        import folium

        # Load data
        data = pd.read_csv('kishi_osek_river_data.csv')

        # Define a threshold for extreme floods (you may need to adjust this value)
        threshold = 10  # meters

        # Find years with extreme floods
        extreme_flood_years = data[data['water_level'] > threshold]['year'].tolist()

        # Check if the current year is an extreme flood year
        current_year = data.iloc[-1]['year']
        current_water_level = data.iloc[-1]['water_level']
        if current_water_level > threshold:
            print(f"The current year ({current_year}) is an extreme flood year.")
        else:
            print(f"The current year ({current_year}) is not an extreme flood year.")

        # Visualize the results on a map (you may need to provide latitude and longitude data for each year)
        m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10)
        for index, row in data[data['year'].isin(extreme_flood_years)].iterrows():
            folium.CircleMarker([row['lat'], row['lon']], radius=5, color='red', fill=True, fill_color='red').add_to(m)
        m.save("200.html")