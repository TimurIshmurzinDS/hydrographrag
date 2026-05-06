# Импорт необходимых библиотек
import folium
from folium.plugins import MarkerCluster

# Шаг 2: Загрузка данных о реке Коктал
# Для примера используем координаты точек, которые могут представлять маршрут реки Коктал.
# В реальном проекте данные должны быть загружены из открытых источников или файла GeoJSON.

river_koktal_coords = [
    [42.8503, 74.6192],
    [42.8510, 74.6200],
    [42.8515, 74.6210],
    [42.8520, 74.6220],
    [42.8530, 74.6230]
]

# Шаг 3: Создание карты с использованием `folium`
m = folium.Map(location=[42.8515, 74.6210], zoom_start=14)

# Добавление маршрута реки Коктал на карту
folium.PolyLine(river_koktal_coords, color="blue", weight=2.5, opacity=1).add_to(m)

# Шаг 4: Добавление элементов игры
# Создание кластера маркеров для объектов игры
marker_cluster = MarkerCluster().add_to(m)

# Пример добавления маркера корабля игрока
folium.Marker(
    location=[42.8510, 74.6200],
    popup='Ваш корабль',
    icon=folium.Icon(color='green')
).add_to(marker_cluster)

# Пример добавления маркеров астероидов
asteroids = [
    [42.8505, 74.6195],
    [42.8525, 74.6225]
]

for coord in asteroids:
    folium.Marker(
        location=coord,
        popup='Астероид',
        icon=folium.Icon(color='red')
    ).add_to(marker_cluster)

# Пример добавления маркера станции
station = [42.8515, 74.6210]
folium.Marker(
    location=station,
    popup='Станция Коктал',
    icon=folium.Icon(color='blue')
).add_to(marker_cluster)

# Шаг 5: Сохранение карты
m.save("239.html")