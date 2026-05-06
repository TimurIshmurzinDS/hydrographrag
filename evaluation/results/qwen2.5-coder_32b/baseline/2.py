import folium
import requests
from datetime import datetime

# Предположим, что у нас есть API для получения данных с датчиков уровня воды.
# URL API и параметры запроса могут отличаться в зависимости от реального источника данных.

API_URL = "https://api.example.com/water_level"
PARAMS = {
    'river': 'Karatal River',
    'sensor_id': '12345',  # Предположительный ID датчика
    'timestamp': datetime.now().isoformat()
}

# Функция для получения данных с API
def get_sensor_data(api_url, params):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при получении данных: {response.status_code}")

# Функция для анализа статуса датчика
def analyze_sensor_status(data):
    status = data.get('status')
    water_level = data.get('water_level')
    
    if status == 'active':
        return f"Датчик работает. Текущий уровень воды: {water_level} м."
    else:
        return "Датчик не работает."

# Получение данных с датчика
sensor_data = get_sensor_data(API_URL, PARAMS)

# Анализ статуса датчика
status_message = analyze_sensor_status(sensor_data)
print(status_message)

# Координаты места расположения датчика (примерные координаты)
latitude = 42.8746
longitude = 74.5910

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Добавление маркера на карту с информацией о датчике
folium.Marker(
    [latitude, longitude],
    popup=status_message,
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты в файл 2.html
m.save("2.html")