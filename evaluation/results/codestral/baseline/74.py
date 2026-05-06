python
        import pandas as pd
        import numpy as np
        import folium
        from scipy import stats

        # Load sensor data
        df = pd.read_csv('sensor_data.csv')

        # Calculate Z-score for each measurement
        z_scores = np.abs(stats.zscore(df['measurements']))

        # Define a threshold to identify outliers (e.g., Z-score > 3)
        threshold = 3

        # Identify anomalies
        df['anomaly'] = z_scores > threshold

        # Create a base map
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

        # Add markers for anomalies on the map
        for index, row in df[df['anomaly']].iterrows():
            folium.Marker([row['latitude'], row['longitude']]).add_to(m)

        # Save the final map
        m.save("74.html")