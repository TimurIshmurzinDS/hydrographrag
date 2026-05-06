import requests
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть API для получения данных о уровне воды реки Kumbel.
# Для примера используем моковые данные.
api_url = "https://example.com/api/water_level/kumbel_river/latest"

response = requests.get(api_url)
data = response.json()

# Предполагаемый формат данных:
# {
#     "measurements": [
#         {"latitude": 45.032, "longitude": 38.976, "water_level": 120.5},
#         {"latitude": 45.045, "longitude": 38.989, "water_level": 119.8}
#     ]
# }

# Шаг 2: Обработка данных
measurements = data.get("measurements", [])

# Шаг 3: Подготовка к визуализации
map_center = [45.037, 38.982]  # примерные координаты центра карты

# Создание интерактивной карты с помощью folium
m = folium.Map(location=map_center, zoom_start=12)

# Добавление маркеров на карту для каждого измерения уровня воды
for measurement in measurements:
    lat = measurement["latitude"]
    lon = measurement["longitude"]
    level = measurement["water_level"]
    
    popup_text = f"Уровень воды: {level} м"
    folium.Marker([lat, lon], popup=popup_text).add_to(m)

# Шаг 4 и 5: Визуализация на карте и сохранение результата
m.save("13.html")