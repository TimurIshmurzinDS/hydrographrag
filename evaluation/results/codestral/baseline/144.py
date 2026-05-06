python
         import pandas as pd
         import geopandas as gpd
         import folium
         # Load data
         water_level_sensors = gpd.read_file('water_level_sensors.geojson')
         # Check for alerts
         alerts = water_level_sensors['alert'].tolist()
         if any(alerts):
             print("There are alerts from water level sensors in the Il River basin.")
         else:
             print("There are no alerts from water level sensors in the Il River basin.")
         # Visualize data on map
         m = folium.Map(location=[water_level_sensors['geometry'].centroid.y.mean(), water_level_sensors['geometry'].centroid.x.mean()], zoom_start=10)
         def style_function(feature):
             if feature['properties']['alert']:
                 return {'fillColor': 'red', 'color': 'red'}
             else:
                 return {'fillColor': 'green', 'color': 'green'}
         folium.GeoJson(water_level_sensors, style_function=style_function).add_to(m)
         m.save("144.html")