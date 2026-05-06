import folium
import requests

# Шаг 1: Сбор данных о реке Кумбель из OpenStreetMap
def get_osm_data(query):
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&polygon=1"
    response = requests.get(url)
    return response.json()

# Получаем данные о реке Кумбель
osm_data = get_osm_data("Река Кумбель")

if not osm_data:
    raise ValueError("Данные о реке Кумбель не найдены.")

# Выбираем первый результат (предполагается, что это нужная река)
river_data = osm_data[0]

# Шаг 2: Обработка данных
# Получаем координаты линии реки из поля 'polygonpoints'
if 'polygonpoints' in river_data:
    coordinates = river_data['polygonpoints']
else:
    raise ValueError("Координаты реки Кумбель не найдены.")

# Шаг 3: Визуализация на карте
# Создаем карту с центром в средней точке реки
center_lat = sum(lat for lat, lon in coordinates) / len(coordinates)
center_lon = sum(lon for lat, lon in coordinates) / len(coordinates)

m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Добавляем линию реки на карту
folium.PolyLine(locations=coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

# Сохраняем карту в файл
m.save("243.html")