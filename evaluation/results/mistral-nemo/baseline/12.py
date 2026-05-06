import geopandas as gpd
import pandas as pd
import folium

# Загружаем данные о местоположении сенсора и его показаниях
sensor_data = pd.read_csv('sensor_data.csv')
river_gdf = gpd.read_file('prokhodnaya_river.shp')

# Создаем векторный слой для местоположения сенсора на карте реки Прокходная
sensor_gdf = gpd.GeoDataFrame(sensor_data, geometry=gpd.points_from_xy(sensor_data['longitude'], sensor_data['latitude']))
sensor_gdf.crs = river_gdf.crs

# Визуализируем данные о показаниях сенсора на карте реки Прокходная
m = folium.Map(location=[river_gdf.centroid.y.mean(), river_gdf.centroid.x.mean()], zoom_start=12)

folium.GeoJson(river_gdf, name='River').add_to(m)
folium.Choropleth(sensor_gdf, name='Sensor Data', columns=['sensor_id', 'value'], key_on='feature.properties.sensor_id', fill_color='YlOrRd', fill_opacity=0.7).add_to(m)

# Анализ данных о показаниях сенсора для выявления ошибок или отклонений от нормальной работы
# (Добавить код анализа данных в зависимости от типа сенсора и его функций)

# Визуализируем результаты анализа на карте реки Прокходная
# (Добавить визуализацию результатов анализа в зависимости от типа сенсора и его функций)

m.save("12.html")