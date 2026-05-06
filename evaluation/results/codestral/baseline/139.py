python
         import geopandas as gpd
         import folium
         from shapely.geometry import Point
         import numpy as np
         # Load data
         rivers = gpd.read_file('rivers.shp')
         sensors = gpd.read_file('sensors.shp')
         # Filter sensors in the Sarykan river region
         sarykan_region = rivers[rivers['name'] == 'Сарыкан'].geometry.unary_union
         sensors_in_region = sensors[sensors.geometry.within(sarykan_region)]
         # Identify anomalies in water level readings (using Z-score for example)
         z_scores = np.abs((sensors_in_region['water_level'] - sensors_in_region['water_level'].mean()) / sensors_in_region['water_level'].std(ddof=0))
         anomalies = sensors_in_region[z_scores > 3]
         # Visualize on map
         m = folium.Map(location=[anomalies.geometry.y.mean(), anomalies.geometry.x.mean()], zoom_start=10)
         for _, r in rivers.iterrows():
             sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
             geo_j = sim_geo.to_json()
             geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
             m.add_child(geo_j)
         for _, s in anomalies.iterrows():
             folium.CircleMarker(location=[s.geometry.y, s.geometry.x], radius=5, color='red').add_to(m)
         m.save("139.html")