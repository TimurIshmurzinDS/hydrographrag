import folium
from geopy.distance import geodesic

# Координаты Альфы Центавра
alpha_centauri_coords = (30.7186, 29.4594)

# Координаты нескольких точек реки Караой
karao_points = [
    (30.7186, 29.4594),  # Пример точки 1
    (30.7186, 29.4594),  # Пример точки 2
    (30.7186, 29.4594)   # Пример точки 3
]

# Расчет расстояния до Альфы Центавра для каждой точки реки Караой
distances = []
for point in karao_points:
    distance = geodesic(point, alpha_centauri_coords).kilometers
    distances.append(distance)

# Определение минимального расстояния
min_distance = min(distances)
min_index = distances.index(min_distance)

# Вывод результата
print(f"Минимальное расстояние до Альфы Центавра: {min_distance:.2f} километров")
print(f"Точка реки Караой с минимальным расстоянием: {karao_points[min_index]}")

# Визуализация на карте
m = folium.Map(location=alpha_centauri_coords, zoom_start=10)

folium.Marker(alpha_centauri_coords, popup='Альфа Центавр').add_to(m)
for point in karao_points:
    folium.Marker(point, popup=f'Точка реки Караой ({karao_points.index(point)})').add_to(m)

m.save("253.html")