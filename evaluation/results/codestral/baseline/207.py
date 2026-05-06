python
        import pandas as pd
        import folium
        from scipy import stats

        # Load data (replace with actual data source)
        emel_data = pd.read_csv('emel_river_data.csv')
        turgen_data = pd.read_csv('turgen_river_data.csv')

        # Data preprocessing
        def preprocess(df):
            df = df.dropna()  # Remove missing values
            df = df[np.abs(stats.zscore(df['water_level'])) < 3]  # Remove outliers
            return df

        emel_data = preprocess(emel_data)
        turgen_data = preprocess(turgen_data)

        # Define extreme water levels as those above the 95th percentile
        def is_extreme(df):
            return df['water_level'] > df['water_level'].quantile(0.95)

        emel_data['is_extreme'] = emel_data.apply(is_extreme, axis=1)
        turgen_data['is_extreme'] = turgen_data.apply(is_extreme, axis=1)

        # Count frequency of extreme water levels per decade
        def count_per_decade(df):
            df['year'] = pd.DatetimeIndex(df['date']).year
            df['decade'] = (df['year'] // 10) * 10
            return df.groupby('decade')['is_extreme'].sum()

        emel_counts = count_per_decade(emel_data)
        turgen_counts = count_per_decade(turgen_data)

        # Visualization (replace with actual coordinates)
        m = folium.Map(location=[55, 37], zoom_start=6)

        for decade in emel_counts.index:
            folium.CircleMarker(
                location=[55, 37],
                radius=emel_counts[decade] * 10,
                color='red',
                fill=True,
                fill_color='red',
                popup=f'Emel River: {decade}s - {emel_counts[decade]} extreme events'
            ).add_to(m)

        for decade in turgen_counts.index:
            folium.CircleMarker(
                location=[56, 38],
                radius=turgen_counts[decade] * 10,
                color='blue',
                fill=True,
                fill_color='blue',
                popup=f'Turgen River: {decade}s - {turgen_counts[decade]} extreme events'
            ).add_to(m)

        m.save("207.html")