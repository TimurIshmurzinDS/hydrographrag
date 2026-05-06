import folium
import requests

# Загрузите данные о датчиках уровня воды с помощью API или из файла
def get_sensor_data():
    # Replace this URL with the actual API endpoint or file path
    url = 'https://example.com/sensors'
    response = requests.get(url)
    return response.json()

# Создайте географическую проекцию и проецируйте координаты датчиков в эту систему координат
def project_coordinates(sensor_data):
    # Assume that the sensor data has 'latitude' and 'longitude' fields
    for sensor in sensor_data:
        sensor['lat'] = float(sensor['latitude'])
        sensor['lon'] = float(sensor['longitude'])
    return sensor_data

# Отобразите местоположение каждого датчика на карте с использованием библиотеки folium
def create_map(sensor_data):
    m = folium.Map(location=[43.25, 76.9], zoom_start=10)  # Start with a map centered on Aksu River

    for sensor in sensor_data:
        status_color = {
            'normal': 'green',
            'maintenance': 'yellow',
            'nonfunctional': 'red'
        }.get(sensor['status'], 'gray')

        folium.CircleMarker(
            location=[sensor['lat'], sensor['lon']],
            radius=5,
            color=status_color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    return m

# Проверить статус каждого датчика и обозначить его цветом на карте
def check_sensor_status(sensor_data):
    # Assume that the sensor data has a 'status' field with possible values: 'normal', 'maintenance', 'nonfunctional'
    for sensor in sensor_data:
        if sensor['status'] == 'normal':
            print(f"Датчик {sensor['id']} работает нормально.")
        elif sensor['status'] == 'maintenance':
            print(f"Датчик {sensor['id']} требует технического обслуживания.")
        else:
            print(f"Датчик {sensor['id']} неработоспособен.")

# Сохранить финальную карту как "61.html"
def save_map(map, filename):
    map.save(filename)

if __name__ == '__main__':
    sensor_data = get_sensor_data()
    projected_sensor_data = project_coordinates(sensor_data)
    check_sensor_status(projected_sensor_data)
    m = create_map(projected_sensor_data)
    save_map(m, "61.html")