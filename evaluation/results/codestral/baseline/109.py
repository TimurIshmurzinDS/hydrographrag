python
         import pandas as pd
         import folium
         from shapely.geometry import Point, LineString
         from geopandas import GeoDataFrame

         # Загрузка данных о реках
         byzhy_data = pd.read_csv('byzhy_river_data.csv')
         lepsy_data = pd.read_csv('lepsy_river_data.csv')

         # Создание GeoDataFrame для каждой реки
         geometry_byzhy = [LineString(zip(byzhy_data['longitude'], byzhy_data['latitude']))]
         gdf_byzhy = GeoDataFrame(byzhy_data, geometry=geometry_byzhy)

         geometry_lepsy = [LineString(zip(lepsy_data['longitude'], lepsy_data['latitude']))]
         gdf_lepsy = GeoDataFrame(lepsy_data, geometry=geometry_lepsy)

         # Оценка доступности водных ресурсов
         def calculate_accessibility(row):
             return (row['length'] * row['width'] * row['depth']) / row['distance_to_livestock_watering_points']

         gdf_byzhy['accessibility'] = gdf_byzhy.apply(calculate_accessibility, axis=1)
         gdf_lepsy['accessibility'] = gdf_lepsy.apply(calculate_accessibility, axis=1)

         # Сравнение доступности водных ресурсов между двумя ручьями
         byzhy_avg_accessibility = gdf_byzhy['accessibility'].mean()
         lepsy_avg_accessibility = gdf_lepsy['accessibility'].mean()

         print(f"Average accessibility for Byzhy River: {byzhy_avg_accessibility}")
         print(f"Average accessibility for Lepsy River: {lepsy_avg_accessibility}")

         # Визуализация результатов на карте с использованием библиотеки folium
         m = folium.Map(location=[gdf_byzhy['latitude'].mean(), gdf_byzhy['longitude'].mean()], zoom_start=10)

         folium.GeoJson(gdf_byzhy[['geometry', 'accessibility']].__geo_interface__, style_function=lambda x: {'color': 'blue' if x['properties']['accessibility'] > lepsy_avg_accessibility else 'red'}).add_to(m)
         folium.GeoJson(gdf_lepsy[['geometry', 'accessibility']].__geo_interface__, style_function=lambda x: {'color': 'blue' if x['properties']['accessibility'] > byzhy_avg_accessibility else 'red'}).add_to(m)

         m.save("109.html")