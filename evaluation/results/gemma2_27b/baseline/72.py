import requests
import folium

# Заменить на реальные URL и параметры API
api_url = "https://example.com/api/water_level"
params = {"rivers": ["Tentek River", "Temirlik River"]}

# Получить данные с API
response = requests.get(api_url, params=params)
data = response.json()

# Обработать данные (пример: извлечь координаты датчиков и уровень воды)
sensor_locations = []
for sensor in data["sensors"]:
    latitude = sensor["latitude"]
    longitude = sensor["longitude"]
    water_level = sensor["water_level"]
    sensor_locations.append((latitude, longitude, water_level))

# Создать карту с folium
m = folium.Map(location=[42.87, 74.59], zoom_start=7)  # Примерные координаты

# Добавить маркеры датчиков на карту
for location in sensor_locations:
    latitude, longitude, water_level = location
    folium.Marker(
        location=[latitude, longitude],
        popup=f"Уровень воды: {water_level}",
        icon=folium.Icon(color='green' if water_level < 2 else 'yellow' if water_level < 4 else 'red'),
    ).add_to(m)

# Сохранить карту
m.save("72.html")