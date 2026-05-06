python
         import geopandas as gpd
         import folium
         # Load rivers data
         rivers = gpd.read_file('rivers.shp')
         # List of target rivers
         target_rivers = ['Улькен Алматы', 'Емель', 'Тентек']
         # Filter rivers to keep only target rivers
         filtered_rivers = rivers[rivers['name'].isin(target_rivers)]
         # Define a function to determine the region of each river (this part may vary depending on your data)
         def get_region(point):
             # Your code here to determine the region based on point coordinates
             pass
         # Apply the function to each river in the filtered GeoDataFrame
         filtered_rivers['region'] = filtered_rivers.geometry.apply(get_region)
         # Group by region and count the number of rivers in each group
         rivers_by_region = filtered_rivers.groupby('region').size().reset_index(name='count')
         # Create a folium map centered around your area of interest
         m = folium.Map(location=[51, 71], zoom_start=6)
         # Add the rivers to the map, colored by region
         for _, r in filtered_rivers.iterrows():
             folium.GeoJson(r['geometry'].__geo_interface__, style_function=lambda x: {'fillColor': 'red' if x['properties']['region'] == 'Region1' else 'blue'}).add_to(m)
         # Save the map as an HTML file
         m.save('105.html')