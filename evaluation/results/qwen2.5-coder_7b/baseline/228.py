import folium
from shapely.geometry import Point, Polygon
import pandas as pd

# Пример данных о реке Аягоз (в реальности нужно использовать актуальные данные)
data = {
    'year': [2018, 2019, 2020, 2021],
    'max_level': [50, 60, 70, 80],
    'min_level': [30, 40, 50, 60]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Определение координат для визуализации (пример)
coordinates = [
    (42.123, 74.567),  # Начальная точка
    (42.124, 74.568),  # Промежуточная точка
    (42.125, 74.569)   # Конечная точка
]

# Создание карты
m = folium.Map(location=[42.123, 74.567], zoom_start=10)

# Добавление маркеров для координат
for coord in coordinates:
    folium.Marker(coord).add_to(m)

# Визуализация данных о реке
folium.PolyLine(coordinates, color='blue').add_to(m)
folium.CircleMarker([42.123, 74.567], radius=5, color='red', fill=True, fill_color='red').add_to(m)

# Сохранение карты
m.save("228.html")