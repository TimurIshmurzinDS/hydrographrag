python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import numpy as np

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
   folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing river names and their annual discharge data
   rivers = [
       {"name": "Turgen River", "discharge": [100, 120, 95, 110, 130]},
       {"name": "Emel River", "discharge": [80, 90, 75, 85, 95]}
   ]

   # Calculate coefficient of variation for each river
   for river in rivers:
       mean_discharge = np.mean(river["discharge"])
       std_deviation = np.std(river["discharge"])
       coeff_variation = std_deviation / mean_discharge
       print(f"Coefficient of variation for {river['name']}: {coeff_variation}")

   # Save the final map
   m.save("202.html")