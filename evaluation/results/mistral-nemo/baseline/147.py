import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Загрузить данные о датчиках и их местоположении.
data = pd.read_csv('sensors.csv')  # Предполагается, что у вас есть файл с данными о датчиках в формате CSV

# 2. Определить географические координаты рек Бутак и Сарыкан.
river_bukhta = (-73.9508, 43.2416)  # Координаты реки Бутак
river_sarykan = (-73.9487, 43.2403)  # Координаты реки Сарыкан

# 3. Отфильтровать датчики, которые находятся вблизи этих рек.
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))
filtered_data = gdf[gdf.distance(gpd.points_from_xy([river_bukhta[0], river_sarykan[0]])).values < 1]

# 4. Проверить каждый из отфильтрованных датчиков на наличие ошибок в данных.
# Предполагается, что у вас есть функция check_errors(), которая возвращает True, если есть ошибки, и False в противном случае.
filtered_data['has_errors'] = filtered_data.apply(check_errors, axis=1)

# 5. Визуализировать результаты на карте с использованием библиотеки `folium`.
m = folium.Map(location=[river_bukhta[1], river_bukhta[0]], zoom_start=16)

for index, row in filtered_data.iterrows():
    if row['has_errors']:
        color = 'red'
    else:
        color = 'green'

    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color=color
    ).add_to(m)

# Сохранить карту в файл HTML.
m.save("147.html")