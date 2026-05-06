import requests
import folium
import json

# Загрузить данные о датчиках уровня с помощью API или импортировать файл данных
def load_sensor_data():
    # Replace this URL with the actual API endpoint or file path
    url = "https://example.com/sensor_data.json"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

# Фильтровать данные по имени реки и извлекать необходимые атрибуты
def filter_and_extract_sensor_data(data, river_name):
    filtered_data = [d for d in data if d['river'] == river_name]
    extracted_data = [(d['latitude'], d['longitude'], d['water_level'], d['last_measurement_time']) for d in filtered_data]
    return extracted_data

# Создать точечный слой и добавить его на карту с помощью folium
def create_sensor_layer(data, map):
    sensor_cluster = folium.MarkerCluster().add_to(map)
    for lat, lon, water_level, measurement_time in data:
        folium.Marker([lat, lon], popup=f"Уровень воды: {water_level}\nВремя последнего измерения: {measurement_time}").add_to(sensor_cluster)
    return map

# Основная функция для выполнения задачи
def main():
    # Загрузить данные о датчиках уровня
    sensor_data = load_sensor_data()

    # Отфильтровать и извлечь данные для Tentek River и Temirlik River
    tentek_data = filter_and_extract_sensor_data(sensor_data, "Tentek River")
    temirlik_data = filter_and_extract_sensor_data(sensor_data, "Temirlik River")

    # Создать карту с помощью folium
    map = folium.Map(location=[41.0082, 69.2401], zoom_start=7)  # Замените координаты на центр вашей области интереса

    # Добавить точечный слой для Tentek River и Temirlik River
    create_sensor_layer(tentek_data, map)
    create_sensor_layer(temirlik_data, map)

    # Сохранить карту в формате HTML
    map.save("72.html")

if __name__ == "__main__":
    main()