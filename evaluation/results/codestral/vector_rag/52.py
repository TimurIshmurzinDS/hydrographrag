python
   import geopandas as gpd
   import folium
   from shapely import wkt
   from statsmodels.tsa.arima_model import ARIMA
   import pandas as pd

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Load water level data for Sarykan River (assuming it's in a CSV file)
   water_level = pd.read_csv('water_level_data.csv', index_col='Date', parse_dates=True)

   # Fit ARIMA model to the data
   model = ARIMA(water_level['Water_level_Value'], order=(5,1,0))
   model_fit = model.fit(disp=0)

   # Make predictions for the next season (assuming we have 365 days in a year and 90 days in a season)
   forecast = model_fit.forecast(steps=90)[0]

   # Save the final map
   m.save("52.html")