python
         # Import necessary libraries
         import pandas as pd
         import geopandas as gpd
         import folium
         from shapely.geometry import Point

         # Load sensor data
         data = pd.read_csv('batareyka_river_sensor_data.csv')

         # Convert data to GeoDataFrame
         geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
         gdf = gpd.GeoDataFrame(data, geometry=geometry)

         # Create a map centered around Batareyka River
         m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=10)

         # Add sensor data points to the map
         for idx, row in gdf.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']],
                                 radius=5,
                                 color='red',
                                 fill=True,
                                 fill_color='red').add_to(m)

         # Analyze sensor data and determine optimal location for spacecraft construction
         # This step is not included in the code as it requires domain-specific knowledge and analysis

         # Save the map
         m.save("220.html")