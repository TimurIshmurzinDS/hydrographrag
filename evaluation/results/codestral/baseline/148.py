python
         import pandas as pd
         import geopandas as gpd
         import folium
         # Load data
         water_levels = pd.read_csv('water_levels.csv')
         rivers = gpd.read_file('rivers.shp')
         # Merge data
         merged = rivers.merge(water_levels, on='river_id', how='inner')
         # Filter high water levels
         high_water = merged[merged['last_measurement'] > merged['average_level']]
         # Create map
         m = folium.Map(location=[55.751244, 37.618423], zoom_start=4)
         # Add rivers to map
         for _, r in high_water.iterrows():
             sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
             geo_j = sim_geo.to_json()
             geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
             folium.Popup(r['river_name'] + ': High water level').add_to(geo_j)
             geo_j.add_to(m)
         # Save map
         m.save("148.html")