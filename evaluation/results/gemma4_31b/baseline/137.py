import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# 1. Создание синтетических данных для демонстрации
# Координаты примерно соответствуют региону бассейнов Или и Каратал (Казахстан/Китай)
basins_data = {
    'name': ['Ili Basin', 'Karatal Basin'],
    'geometry': [
        # Упрощенные полигоны для бассейнов
        Polygon([(42.0, 43.0), (45.0, 43.0), (45.0, 44.5), (42.0, 44.5), (42.0, 43.0)]),
        Polygon([(43.5, 43.5), (44.5, 43.5), (44.5, 44.0), (43.5, 44.0), (43.5, 43.5)])
    ]
}

sensors_data = {
    'sensor_id': [101, 102, 103, 104, 105, 106],
    'lat': [43.5, 43.8, 44.2, 43.7, 45.5, 43.2], # 45.5 - вне бассейнов
    'lon': [43.0, 44.0, 44.1, 43.8, 46.0, 41.0], # 41.0 - вне бассейнов
    'status': ['working', 'faulty', 'working', 'faulty', 'working', 'faulty']
}

# Преобразование в GeoDataFrames
basins_gdf = gpd.GeoDataFrame(basins_data, crs="EPSG:4326")
sensors_df = pd.DataFrame(sensors_data)
sensors_gdf = gpd.GeoDataFrame(
    sensors_df, 
    geometry=gpd.points_from_xy(sensors_df.lon, sensors_df.lat), 
    crs="EPSG:4326"
)

# 2. Пространственная фильтрация (Spatial Join)
# Находим датчики, которые находятся внутри любого из бассейнов
sensors_in_basins = gpd.sjoin(sensors_gdf, basins_gdf, predicate='within')

# 3. Анализ неисправных датчиков
faulty_sensors = sensors_in_basins[sensors_in_basins['status'] == 'faulty']

print(f"Всего датчиков в бассейнах: {len(sensors_in_basins)}")
print(f"Количество неисправных датчиков: {len(faulty_sensors)}")
print(faulty_sensors[['sensor_id', 'status', 'name']])

# 4. Визуализация
# Центрируем карту на среднем значении координат
m = folium.Map(location=[43.7, 43.5], zoom_start=7, tiles='CartoDB positron')

# Добавляем полигоны бассейнов на карту
folium.GeoJson(
    basins_gdf,
    name="River Basins",
    style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'weight': 1, 'fillOpacity': 0.2}
).add_to(m)

# Добавляем датчики на карту
for idx, row in sensors_in_basins.iterrows():
    color = 'red' if row['status'] == 'faulty' else 'green'
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Sensor ID: {row['sensor_id']}<br>Status: {row['status']}<br>Basin: {row['name']}"
    ).add_to(m)

# Сохранение карты
m.save("137.html")