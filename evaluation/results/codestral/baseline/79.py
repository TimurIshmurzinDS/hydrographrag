python
        import pandas as pd
        from scipy import stats
        import folium

        # Load the data
        data = pd.read_csv('turgen_river_data.csv')

        # Convert date column to datetime format
        data['date'] = pd.to_datetime(data['date'])

        # Set date as index
        data.set_index('date', inplace=True)

        # Calculate Z-score for the discharge column
        data['z_score'] = stats.zscore(data['discharge'])

        # Define a threshold for flood detection (e.g., Z-score > 3)
        data['flood'] = data['z_score'].apply(lambda x: 1 if x > 3 else 0)

        # Visualize the results on a map using folium
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

        for index, row in data[data['flood'] == 1].iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='red').add_to(m)

        m.save("79.html")