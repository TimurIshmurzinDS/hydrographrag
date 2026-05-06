python
       import geopandas as gpd
       import folium
       from shapely import wkt
       import matplotlib.pyplot as plt

       # Load the shapefile (assuming it contains water level data for both years)
       gdf = gpd.read_file(r"data/water_level_data.shp")
       gdf = gdf.to_crs('EPSG:4326')

       # Filter the data for 2022 and 2023
       water_level_2022 = gdf[gdf['Date_water_level_Value'].dt.year == 2022]['Water_level_Value']
       water_level_2023 = gdf[gdf['Date_water_level_Value'].dt.year == 2023]['Water_level_Value']

       # Create a plot to compare the water levels
       plt.figure(figsize=(10, 6))
       plt.plot(water_level_2022, label='2022')
       plt.plot(water_level_2023, label='2023')
       plt.title('Water Level Comparison for Sarykan River (2022 vs 2023)')
       plt.xlabel('Time')
       plt.ylabel('Water Level')
       plt.legend()
       plt.show()