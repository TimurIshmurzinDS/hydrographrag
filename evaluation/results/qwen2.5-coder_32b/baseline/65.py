import folium
import requests

# Предполагаемые URL для получения данных с датчиков
aksu_url = "http://example.com/api/aksu_water_level"
byzhy_url = "http://example.com/api/byzhy_water_level"

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def check_sensor(data):
    if data is None or 'water_level' not in data or 'status' not in data:
        return False
    return data['status'] == 'active'

# Получение данных с датчиков
aksu_data = fetch_data(aksu_url)
byzhy_data = fetch_data(byzhy_url)

# Проверка состояния датчиков
aksu_sensor_ok = check_sensor(aksu_data)
byzhy_sensor_ok = check_sensor(byzhy_data)

# Создание карты
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерные

# Добавление маркеров на карту
if aksu_sensor_ok:
    folium.Marker(
        location=[aksu_data['latitude'], aksu_data['longitude']],
        popup=f"Aksu River: Уровень воды {aksu_data['water_level']} м",
        icon=folium.Icon(color='green')
    ).add_to(m)
else:
    folium.Marker(
        location=[aksu_data['latitude'], aksu_data['longitude']],
        popup="Aksu River: Датчик неисправен",
        icon=folium.Icon(color='red')
    ).add_to(m)

if byzhy_sensor_ok:
    folium.Marker(
        location=[byzhy_data['latitude'], byzhy_data['longitude']],
        popup=f"Byzhy River: Уровень воды {byzhy_data['water_level']} м",
        icon=folium.Icon(color='green')
    ).add_to(m)
else:
    folium.Marker(
        location=[byzhy_data['latitude'], byzhy_data['longitude']],
        popup="Byzhy River: Датчик неисправен",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("65.html")