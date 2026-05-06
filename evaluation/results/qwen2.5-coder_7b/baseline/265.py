import folium
from folium.plugins import HeatMap

# Пример данных: местоположение реки Эмел и источники загрязнения
river_points = [
    (52.406, 13.489),  # Начало реки
    (52.410, 13.500),
    (52.415, 13.510),
    (52.420, 13.520),
    (52.425, 13.530)
]

pollution_sources = [
    (52.412, 13.505),  # Источник загрязнения 1
    (52.418, 13.525)   # Источник загрязнения 2
]

# Создание карты
m = folium.Map(location=[52.410, 13.500], zoom_start=13)

# Добавление линии реки
folium.PolyLine(river_points, color='blue', weight=2.5, opacity=1).add_to(m)

# Добавление точек загрязнения
for point in pollution_sources:
    folium.Marker(point, popup="Источник загрязнения", icon=folium.Icon(color='red')).add_to(m)

# Создание теплового картографа для демонстрации распространения загрязнения
heatmap_data = []
for source in pollution_sources:
    for point in river_points:
        distance = folium.plugins.distance(source, point)
        heatmap_data.append([point[0], point[1], 1 / (distance + 1)])  # Уменьшаем значение с увеличением расстояния

HeatMap(heatmap_data).add_to(m)

# Сохранение карты
m.save("265.html")