python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd
   from scipy.stats import pearsonr, spearmanr

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Load the precipitation and discharge data for Urzhar River and Byzhy River
   data = pd.read_csv('data/hydro_data.csv')

   # Calculate Pearson correlation coefficient
   pearson_corr, _ = pearsonr(data['precipitation'], data['discharge'])

   # Calculate Spearman rank correlation coefficient
   spearman_corr, _ = spearmanr(data['precipitation'], data['discharge'])

   print("Pearson Correlation Coefficient:", pearson_corr)
   print("Spearman Rank Correlation Coefficient:", spearman_corr)

   # Save the final map
   m.save("199.html")