python
         import pandas as pd
         import geopandas as gpd
         from scipy.interpolate import griddata
         import numpy as np
         import folium
         # Load data
         data_2022 = pd.read_csv('water_levels_2022.csv')
         data_2023 = pd.read_csv('water_levels_2023.csv')
         # Check for missing values or errors in the data
         data_2022 = data_2022.dropna()
         data_2023 = data_2023.dropna()
         # Create a GeoDataFrame from the data
         gdf_2022 = gpd.GeoDataFrame(data_2022, geometry=gpd.points_from_xy(data_2022.longitude, data_2022.latitude))
         gdf_2023 = gpd.GeoDataFrame(data_2023, geometry=gpd.points_from_xy(data_2023.longitude, data_2023.latitude))
         # Create a map centered around the Sarykan River
         m = folium.Map(location=[gdf_2022.geometry.y.mean(), gdf_2022.geometry.x.mean()], zoom_start=10)
         # Add measurement points to the map for both years
         for idx, row in gdf_2022.iterrows():
             folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
         for idx, row in gdf_2023.iterrows():
             folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color='red', fill=True, fill_color='red').add_to(m)
         # Interpolate water level data to create a surface for each year
         xi = np.linspace(gdf_2022.geometry.x.min(), gdf_2022.geometry.x.max(), 100)
         yi = np.linspace(gdf_2022.geometry.y.min(), gdf_2022.geometry.y.max(), 100)
         zi_2022 = griddata((gdf_2022.geometry.x, gdf_2022.geometry.y), gdf_2022.water_level, (xi[None,:], yi[:,None]), method='cubic')
         zi_2023 = griddata((gdf_2023.geometry.x, gdf_2023.geometry.y), gdf_2023.water_level, (xi[None,:], yi[:,None]), method='cubic')
         # Add the interpolated surfaces to the map as heatmaps
         folium.raster_layers.ImageOverlay(zi_2022, bounds=[[yi.min(), xi.min()], [yi.max(), xi.max()]], opacity=0.5, colormap='blue').add_to(m)
         folium.raster_layers.ImageOverlay(zi_2023, bounds=[[yi.min(), xi.min()], [yi.max(), xi.max()]], opacity=0.5, colormap='red').add_to(m)
         # Save the map as an HTML file
         m.save("46.html")