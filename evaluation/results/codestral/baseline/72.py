python
         import pandas as pd
         import geopandas as gpd
         import folium
         # Load data
         data = pd.read_csv('sensor_data.csv')
         # Check and preprocess data
         data = data.dropna()
         data['status'] = data['status'].apply(lambda x: 'Normal' if x == 1 else 'Abnormal')
         # Create GeoDataFrame
         gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))
         # Create map
         m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=10)
         # Add sensor data layer to map
         for _, r in gdf.iterrows():
             if r['status'] == 'Normal':
                 color = 'green'
             else:
                 color = 'red'
             folium.CircleMarker(location=[r['latitude'], r['longitude']], radius=5, color=color, fill_color=color).add_to(m)
         # Save map
         m.save("72.html")