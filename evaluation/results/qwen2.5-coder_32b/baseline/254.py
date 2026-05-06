import folium
import random
from shapely.geometry import LineString

# Пример данных о координатах точек русла реки Шилик (широта, долгота)
river_points = [
    [56.1234, 80.1234],
    [56.1244, 80.1244],
    [56.1254, 80.1254],
    [56.1264, 80.1264],
    [56.1274, 80.1274]
]

# Создание объекта LineString для вычисления длины русла
river_line = LineString(river_points)

# Вычисление прямолинейного расстояния между начальной и конечной точками
start_point = river_points[0]
end_point = river_points[-1]
straight_distance = ((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2)**0.5

# Вычисление извилистости русла реки
winding_factor = river_line.length / straight_distance

# Генерация случайных чисел на основе извилистости
random_numbers = [random.uniform(0, winding_factor) for _ in range(len(river_points))]

# Создание карты с использованием folium
m = folium.Map(location=[56.1254, 80.1254], zoom_start=13)

# Добавление линии русла реки на карту
folium.PolyLine(river_points, color="blue", weight=2.5, opacity=1).add_to(m)

# Добавление маркеров с случайными числами на карту
for point, number in zip(river_points, random_numbers):
    folium.Marker(
        location=point,
        popup=f"Случайное число: {number:.4f}",
        icon=folium.Icon(color="red")
    ).add_to(m)

# Сохранение карты в файл 254.html
m.save("254.html")

print(f"Извилистость русла реки Шилик: {winding_factor}")
print(f"Сгенерированные случайные числа: {random_numbers}")