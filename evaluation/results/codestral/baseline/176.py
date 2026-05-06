python
         import geopandas as gpd
         from shapely.ops import nearest_points
         import folium
         # Load data
         terisbutak = gpd.read_file('terisbutak.geojson')
         talgar = gpd.read_file('talgar.geojson')
         # Reproject if necessary
         if terisbutak.crs != talgar.crs:
             terisbutak = terisbutak.to_crs(talgar.crs)
         # Calculate distances
         distances = []
         for i, row in terisbutak.iterrows():
             nearest = nearest_points(row['geometry'], talgar.unary_union)[1]
             distance = row['geometry'].distance(nearest)
             distances.append(distance)
         # Find minimum distance and corresponding points
         min_distance = min(distances)
         min_index = distances.index(min_distance)
         nearest_point_terisbutak = terisbutak.iloc[min_index]['geometry']
         nearest_point_talgar = talgar.geometry.intersects(nearest_point_terisbutak).any()
         # Visualize results
         m = folium.Map(location=[51, 71], zoom_start=10)
         folium.GeoJson(terisbutak).add_to(m)
         folium.GeoJson(talgar).add_to(m)
         folium.Marker([nearest_point_terisbutak.y, nearest_point_terisbutak.x], icon=folium.Icon(color='red')).add_to(m)
         folium.Marker([nearest_point_talgar.y, nearest_point_talgar.x], icon=folium.Icon(color='blue')).add_to(m)
         m.save("176.html")