import requests
import folium
import json

# Шаг 1: Получение данных об уровне воды реки Осек в реальном времени
def get_water_level():
    # Замените 'YOUR_API_KEY' и 'YOUR_API_URL' на действительные API-ключ и URL
    api_key = 'YOUR_API_KEY'
    api_url = 'YOUR_API_URL'

    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data['water_level']
    else:
        print(f"Error: Unable to fetch water level data. Status code: {response.status_code}")
        return None

# Шаг 2: Анализ данных для определения текущего уровня воды во время паводка
def analyze_water_level(water_level):
    # Определите пороговый уровень воды для паводка
    flood_threshold = 5.0

    if water_level > flood_threshold:
        print(f"Текущий уровень воды на реке Осек в период паводка: {water_level} м")
    else:
        print("Паводок не происходит.")

# Шаг 3: Визуализация данных на карте с помощью библиотеки Folium
def visualize_on_map(water_level):
    # Координаты реки Осек для центрирования карты
    osek_river_coords = (52.7069, -1.8446)

    m = folium.Map(location=osek_river_coords, zoom_start=13)

    # Отображение текущего уровня воды на реке Осек
    folium.Marker(location=osek_river_coords, popup=f"Уровень воды: {water_level} м").add_to(m)

    # Сохранение карты в файл HTML
    m.save("26.html")

# Основной код
if __name__ == "__main__":
    water_level = get_water_level()
    if water_level is not None:
        analyze_water_level(water_level)
        visualize_on_map(water_level)