import folium
import requests
from shapely.geometry import LineString

# Функция для получения данных о реке из OpenStreetMap через Nominatim API
def get_river_coordinates(river_name):
    url = f"https://nominatim.openstreetmap.org/search?q={river_name}&format=json&polygon=1"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        raise ValueError(f"Не удалось найти реку {river_name}")
    
    # Предполагаем, что первая запись - это нужная нам река
    river_data = data[0]
    coordinates = river_data['geojson']['coordinates']
    
    return coordinates

# Получение координат рек Тентек и Быж
tentek_coords = get_river_coordinates("Тентек")
byzh_coords = get_river_coordinates("Быж")

# Преобразование координат в LineString для удобства работы
tentek_line = LineString(tentek_coords[0])
byzh_line = LineString(byzh_coords[0])

# Нахождение самой северной точки реки Тентек (самого верхнего истка)
tentek_top_point = max(tentek_line.coords, key=lambda x: x[1])

# Координаты самого верхнего истка реки Тентек
tentek_top_coords = tentek_top_point

# Вывод координат для сравнения
print(f"Координаты самого верхнего истка реки Тентек: {tentek_top_coords}")
print(f"Координаты реки Быж: {byzh_line.coords[0]}")

# Создание карты с помощью folium
m = folium.Map(location=[56, 37], zoom_start=10)

# Добавление линий рек на карту
folium.PolyLine(tentek_coords[0], color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(byzh_coords[0], color="green", weight=2.5, opacity=1).add_to(m)

# Добавление маркеров для истка реки Тентек и первой точки реки Быж
folium.Marker(tentek_top_coords, popup="Исток реки Тентек", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(byzh_line.coords[0], popup="Начало реки Быж", icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты в файл
m.save("94.html")