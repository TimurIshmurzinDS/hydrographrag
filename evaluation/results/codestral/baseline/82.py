python
         import geopandas as gpd
         import folium
         # Load data
         posts = gpd.read_file('posts.shp')
         # Define critical flood level
         critical_level = 1000  # m3/s, replace with actual value
         # Add new attribute to indicate if post discharge exceeds critical level
         posts['flood'] = posts['discharge'].apply(lambda x: 'Yes' if x > critical_level else 'No')
         # Create map centered on the river
         m = folium.Map(location=[posts.geometry.y.mean(), posts.geometry.x.mean()], zoom_start=10)
         # Add points to map, colored by flood attribute
         for idx, row in posts.iterrows():
             color = 'red' if row['flood'] == 'Yes' else 'blue'
             folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color=color).add_to(m)
         # Save map as HTML file
         m.save('82.html')