import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Подготовка данных
data_baskan = pd.read_csv('baskan_river_data.csv')
data_prokhodnaya = pd.read_csv('prokhodnaya_river_data.csv')

# Шаг 2: Геопространственный анализ
gdf_baskan = gpd.GeoDataFrame(data_baskan, geometry=gpd.points_from_xy(data_baskan['longitude'], data_baskan['latitude']))
gdf_prokhodnaya = gpd.GeoDataFrame(data_prokhodnaya, geometry=gpd.points_from_xy(data_prokhodnaya['longitude'], data_prokhodnaya['latitude']))

# Шаг 3: Анализ данных
# TODO: Добавить код для анализа данных о сезонном расходе воды на реках Baskan River и Prokhodnaya River

# Шаг 4: Прогнозирование половодья
# TODO: Добавить код для прогнозирования весеннего половодья на обеих реках

# Шаг 5: Визуализация результатов
m = folium.Map(location=[gdf_baskan['latitude'].mean(), gdf_baskan['longitude'].mean()], zoom_start=8)

folium.GeoJson(gdf_baskan[['geometry']]).add_to(m)
folium.GeoJson(gdf_prokhodnaya[['geometry']]).add_to(m)

# Шаг 6: Сохранение результатов
m.save("77.html")