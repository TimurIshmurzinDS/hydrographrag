python
        import pandas as pd
        import numpy as np
        import folium

        # Load data
        data = pd.read_csv('talgar_river_data.csv')

        # Calculate NDVI
        data['NDVI'] = (data['NIR'] - data['Red']) / (data['NIR'] + data['Red'])

        # Create a map centered around the Talgar River
        m = folium.Map(location=[42.35, 71.9], zoom_start=10)

        # Add NDVI values to the map
        for index, row in data.iterrows():
            folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                                radius=5,
                                color='green' if row['NDVI'] > 0 else 'red',
                                fill_color='green' if row['NDVI'] > 0 else 'red',
                                popup=f"NDVI: {row['NDVI']}").add_to(m)

        # Save the map
        m.save("270.html")