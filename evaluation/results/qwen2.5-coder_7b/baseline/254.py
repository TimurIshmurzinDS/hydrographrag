import folium
from shapely.geometry import LineString
import random

# Определяем координаты русла реки Шилик (пример данных)
coordinates = [
    (50.123, 49.876),
    (50.124, 49.877),
    (50.125, 49.878),
    # Добавьте больше точек для более точного измерения извилистости
]

# Создаем объект LineString из координат
river_line = LineString(coordinates)

# Функция для вычисления извилистости линии
def calculate_meandering_factor(line):
    length = line.length
    perimeter = sum([line[i].distance(line[i+1]) for i in range(len(line)-1)])
    meandering_factor = perimeter / length
    return meandering_factor

# Вычисляем извилистость русла реки Шилик
meandering_factor = calculate_meandering_factor(river_line)

# Генерация случайных чисел на основе извилистости
def generate_random_numbers(factor, count):
    random_numbers = []
    for _ in range(count):
        random_number = random.uniform(0, factor)
        random_numbers.append(random_number)
    return random_numbers

# Генерируем 10 случайных чисел
random_numbers = generate_random_numbers(meandering_factor, 10)

# Визуализация на карте с использованием folium
m = folium.Map(location=[50.124, 49.877], zoom_start=13)

folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

for coord in coordinates:
    folium.Marker(coord, popup=f"Random Number: {random_numbers.pop(0):.2f}").add_to(m)

m.save("254.html")