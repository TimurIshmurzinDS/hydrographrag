python
         import folium
         import geopandas as gpd
         # Load data
         water_level_sensors = gpd.read_file('water_level_sensors.geojson')
         # Create map
         m = folium.Map(location=[water_level_sensors['geometry'].y.mean(), water_level_sensors['geometry'].x.mean()], zoom_start=10)
         # Add sensors layer to the map
         for i, row in water_level_sensors.iterrows():
             if row['status'] == 'working':
                 color = 'green'
             else:
                 color = 'red'
             folium.CircleMarker(location=[row['geometry'].y, row['geometry'].x], radius=5, color=color, fill_color=color).add_to(m)
         # Save the map to a file
         m.save("2.html")