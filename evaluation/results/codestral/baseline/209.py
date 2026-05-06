python
         import folium
         from osgeo import gdal, ogr
         import numpy as np
         import pandas as pd
         from scipy.stats import genextreme

         # Load data
         dem = gdal.Open('dem_data.tif')
         soil = gdal.Open('soil_data.tif')
         rainfall_data = pd.read_csv('rainfall_data.csv')

         # Model extreme rainfall
         model = genextreme(c=-0.1, loc=rainfall_data.mean(), scale=rainfall_data.std())
         extreme_rainfall = model.rvs(size=1000)

         # Model water flow and flood risk
         # This is a simplified example and may require more complex models in practice
         def calculate_flood_risk(dem, soil, rainfall):
             return np.clip((dem - soil * 0.1) / (rainfall + 1), 0, 1)

         flood_risk = calculate_flood_risk(dem.ReadAsArray(), soil.ReadAsArray(), extreme_rainfall)

         # Visualize results on a map
         m = folium.Map(location=[55, 60], zoom_start=10)
         folium.raster_layers.ImageOverlay(
             image=flood_risk,
             bounds=[[dem.GetGeoTransform()[3], dem.GetGeoTransform()[0]], [dem.GetGeoTransform()[3] + dem.RasterYSize * dem.GetGeoTransform()[5], dem.GetGeoTransform()[0] + dem.RasterXSize * dem.GetGeoTransform()[1]]],
             colormap=lambda x: (int(255 * x), 0, int(255 * (1 - x)), 255)
         ).add_to(m)
         m.save("209.html")