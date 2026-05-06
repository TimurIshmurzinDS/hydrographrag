import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Загрузить данные о реках в формате вектора из источника данных.
rivers = gpd.read_file("rivers.shp")

# 2. Фильтровать данные, чтобы получить только реки Текес и Сарыкан.
tekes_river = rivers[rivers['name'] == 'Текес']
sarykhan_river = rivers[rivers['name'] == 'Сарыкан']

# 3. Выполнить операцию объединения рек по их истокам и устьям для получения единой сети рек.
merged_rivers = gpd.GeoDataFrame(geometry=tekes_river.geometry.append(sarykhan_river.geometry))

# 4. Анализировать конфигурацию речной сети с помощью различных метрик, таких как длина реки, площадь водосборного бассейна, средний наклон и т.д.
merged_rivers['length'] = merged_rivers.apply(lambda row: row.geometry.length, axis=1)
merged_rivers['basin_area'] = merged_rivers.apply(lambda row: row.geometry.buffer(500).area, axis=1)  # примерный размер водосборного бассейна
merged_rivers['slope'] = merged_rivers.apply(lambda row: row.geometry.slope.mean(), axis=1)

# 5. Визуализировать результаты анализа на карте с использованием библиотеки `folium`.
m = folium.Map(location=[np.mean(merged_rivers.geometry.y), np.mean(merged_rivers.geometry.x)], zoom_start=8)
for _, row in merged_rivers.iterrows():
    folium.GeoJson(row.geometry, style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Сохранить карту в формате HTML
m.save("180.html")