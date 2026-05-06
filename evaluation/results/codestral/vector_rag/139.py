python
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Load the basin data
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Initialize folium map
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Add the basin to the map
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Assuming we have a dataframe df containing water level data for Sarykan River
   # We can add markers to the map for each anomalous water level reading
   anomalies = df[df['Water_level_Value'] > df['Water_level_Value'].mean() + 3*df['Water_level_Value'].std()]
   for i, row in anomalies.iterrows():
       folium.Marker([row['Latitude'], row['Longitude']], popup=f"Anomalous water level: {row['Water_level_Value']} at {row['Date_water_level_Value']}").add_to(m)

   # Save the final map
   m.save("139.html")