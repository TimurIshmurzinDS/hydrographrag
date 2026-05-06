python
         import pandas as pd
         import geopandas as gpd
         import folium
         # Load data
         hydro_posts = gpd.read_file('hydro_posts.geojson')
         # Get water levels (replace with actual API or data source)
         water_levels = pd.DataFrame({'id': [1, 2, 3], 'water_level': [5.2, 4.8, 6.1]})
         # Merge data
         merged_data = hydro_posts.merge(water_levels, left_on='id', right_on='id')
         # Create map
         m = folium.Map(location=[merged_data['geometry'].y.mean(), merged_data['geometry'].x.mean()], zoom_start=10)
         # Add markers to map
         for i, row in merged_data.iterrows():
             folium.Marker([row['geometry'].y, row['geometry'].x], popup=f"Water level: {row['water_level']} m").add_to(m)
         # Save map
         m.save("63.html")