python
        import pandas as pd
        import numpy as np
        from scipy import stats
        import folium

        # Load data
        snowmelt_data = pd.read_csv('snowmelt_data.csv')
        waterlevel_data = pd.read_csv('waterlevel_data.csv')

        # Data preprocessing
        merged_data = pd.merge(snowmelt_data, waterlevel_data, on='date')
        merged_data = merged_data.dropna()

        # Statistical analysis
        correlation, p_value = stats.pearsonr(merged_data['snowmelt'], merged_data['waterlevel'])
        print(f'Correlation coefficient: {correlation}, p-value: {p_value}')

        # Visualization on a map
        m = folium.Map(location=[53, 108], zoom_start=6)

        for i in range(len(merged_data)):
            folium.CircleMarker(
                location=[merged_data['lat'][i], merged_data['lon'][i]],
                radius=np.sqrt(abs(merged_data['snowmelt'][i])*5),
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

        m.save("162.html")