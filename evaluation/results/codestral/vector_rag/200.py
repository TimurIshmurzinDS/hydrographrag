python
   import geopandas as gpd
   import folium
   from shapely import wkt
   import pandas as pd

   # Load the shapefile and convert to CRS 'EPSG:4326'
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

   # Add the basin to the map using folium.GeoJson
   folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Hardcoded list of dictionaries containing Coordinates (WKT) from the context
   observations = [{'year': 2010, 'discharge': 500}, {'year': 2011, 'discharge': 600}, ...]

   # Convert the list of dictionaries to a DataFrame
   df = pd.DataFrame(observations)

   # Calculate the mean discharge and standard deviation
   mean_discharge = df['discharge'].mean()
   std_deviation = df['discharge'].std()

   # Define a threshold for extreme floods (e.g., 2 standard deviations above the mean)
   threshold = mean_discharge + 2 * std_deviation

   # Filter the DataFrame to include only years with discharge above the threshold
   extreme_floods = df[df['discharge'] > threshold]

   # Print the years of extreme floods
   print("Years of extreme floods:", extreme_floods['year'].tolist())

   # Save the final map
   m.save("200.html")