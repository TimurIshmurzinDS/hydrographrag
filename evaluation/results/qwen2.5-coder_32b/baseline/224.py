import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с координатами реки Karaoy (longitude, latitude)
data = {
    'latitude': [42.9833, 42.9850, 42.9867, 42.9883, 42.9900],
    'longitude': [71.5167, 71.5183, 71.5200, 71.5217, 71.5233]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Шаг 2: Обработка данных
# Преобразование DataFrame в GeoDataFrame
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Создание линии (траектории реки)
line = LineString([point for point in gdf.geometry])

# Шаг 3: Создание модели робота
# Начальная позиция робота (можно выбрать любую точку на траектории)
start_point = Point(71.5167, 42.9833)

# Алгоритм движения робота по линии (простой пример: движение к следующей точке)
robot_path = [start_point]
for point in gdf.geometry:
    robot_path.append(point)

# Создание линии пути робота
robot_line = LineString(robot_path)

# Шаг 4: Визуализация
# Создание карты с центром в средней точке траектории реки
center_lat = (df['latitude'].min() + df['latitude'].max()) / 2
center_lon = (df['longitude'].min() + df['longitude'].max()) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Добавление траектории реки на карту
folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=5).add_to(m)

# Добавление пути робота на карту
folium.PolyLine(locations=[[p.y, p.x] for p in robot_line.coords], color='red', weight=3).add_to(m)

# Шаг 5: Сохранение карты
m.save("224.html")