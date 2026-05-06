import folium
from shapely.geometry import LineString, Point

# Пример данных о реке Karaoy River (координаты узлов)
karaoy_river_nodes = [
    (39.1234, 45.6789),
    (39.1235, 45.6790),
    (39.1236, 45.6791),
    # Добавьте больше узлов по необходимости
]

# Создание объекта LineString из координат узлов
river_line = LineString(karaoy_river_nodes)

# Создание карты с центром в средней точке пути реки
m = folium.Map(location=river_line.centroid.coords[0], zoom_start=13)

# Добавление пути реки на карту
folium.PolyLine(river_line.coords, color='blue', weight=2.5, opacity=1).add_to(m)

# Добавление маркеров для ключевых точек (например, источника и устья)
source_point = Point(karaoy_river_nodes[0])
sink_point = Point(karaoy_river_nodes[-1])

folium.Marker(source_point.coords[0], popup='Источник', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(sink_point.coords[0], popup='Устье', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("224.html")