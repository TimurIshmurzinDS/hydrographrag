python
         import geopandas as gpd
         import pandas as pd
         import folium
         # Load river data
         river = gpd.read_file('talgar_river.geojson')
         # Load water level data
         water_levels = pd.read_csv('water_levels.csv', parse_dates=['date'])
         # Merge data
         merged = river.merge(water_levels, left_on='id', right_on='river_id')
         # Filter for last water level
         last_water_level = merged[merged['date'] == merged['date'].max()]
         # Create map
         m = folium.Map(location=[last_water_level['lat'].mean(), last_water_level['lon'].mean()], zoom_start=10)
         # Add water level data to map
         for i, row in last_water_level.iterrows():
             folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color='blue', fill=True, fill_color='blue', popup=f"Water Level: {row['water_level']}").add_to(m)
         # Save map
         m.save("3.html")