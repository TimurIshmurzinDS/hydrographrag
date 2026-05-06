import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, LineString

# 1. Создание синтетических данных для демонстрации (так как реальные файлы отсутствуют)
# Координаты примерно соответствуют региону Казахстана
rivers_data = {
    'name': ['Butak', 'Sarykan'],
    'geometry': [
        LineString([(67.1, 48.2), (67.5, 48.5), (68.0, 48.3)]), # Река Бутак
        LineString([(67.8, 48.1), (68.2, 48.4), (68.5, 48.2)])  # Река Сарыкан
    ]
}
rivers_gdf = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")

sensors_data = {
    'sensor_id': [1, 2, 3, 4, 5, 6],
    'status': ['OK', 'Error', 'OK', 'Error', 'OK', 'OK'],
    'geometry': [
        Point(67.2, 48.3), # В районе Бутак (OK)
        Point(67.6, 48.4), # В районе Бутак (Error)
        Point(68.1, 48.3), # В районе Сарыкан (OK)
        Point(68.3, 48.3), # В районе Сарыкан (Error)
        Point(68.4, 48.2), # В районе Сарыкан (OK)
        Point(69.0, 49.0)  # Вне района рек (OK)
    ]
}
sensors_gdf = gpd.GeoDataFrame(sensors_data, crs="EPSG:4326")

# 2. Создание буферной зоны вокруг рек
# Для корректного расчета буфера в метрах переводим в проекционную систему (например, UTM)
# Но для упрощения примера используем градусы (0.1 градуса ~ 11 км)
buffer_dist = 0.1 
rivers_buffer = rivers_gdf.buffer(buffer_dist)
rivers_buffer_gdf = gpd.GeoDataFrame(rivers_gdf, geometry=rivers_buffer, crs="EPSG:4326")

# 3. Пространственная фильтрация датчиков
# Оставляем только те датчики, которые находятся внутри буфера рек
sensors_in_area = gpd.sjoin(sensors_gdf, rivers_buffer_gdf, predicate='within')

# 4. Проверка наличия ошибок
sensors_with_errors = sensors_in_area[sensors_in_area['status'] == 'Error']
all_ok = len(sensors_with_errors) == 0

print(f"Все ли датчики работают без ошибок? {'Да' if all_ok else 'Нет'}")
print(f"Количество датчиков с ошибками в районе рек: {len(sensors_with_errors)}")

# 5. Визуализация
# Центрируем карту по средним координатам рек
m = folium.Map(location=[48.3, 67.8], zoom_start=8)

# Добавляем реки на карту
for idx, row in rivers_gdf.iterrows():
    coords = [(p[1], p[0]) for p in row.geometry.coords]
    folium.PolyLine(coords, color='blue', weight=3, opacity=0.8, popup=row['name']).add_to(m)

# Добавляем датчики на карту
for idx, row in sensors_in_area.iterrows():
    color = 'green' if row['status'] == 'OK' else 'red'
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Sensor {row['sensor_id']}: {row['status']}"
    ).add_to(m)

# Сохранение карты
m.save("147.html")