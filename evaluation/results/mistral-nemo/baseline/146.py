import folium

# Шаг 1: Получение данных о местоположении датчиков
def get_sensor_data():
    # Предполагается, что у нас есть данные о местоположении датчиков в виде списка словарей
    sensor_data = [
        {'name': 'Sensor_Aya_1', 'location': [43.2577, 69.9785], 'status': 'working'},
        {'name': 'Sensor_Toky_1', 'location': [43.2609, 70.0122], 'status': 'not_working'},
        # Добавьте другие датчики по мере необходимости
    ]
    return sensor_data

# Шаг 2: Определение состояния датчиков
def check_sensor_status(sensor_data):
    sensors_to_maintain = []
    for sensor in sensor_data:
        if sensor['status'] == 'not_working':
            sensors_to_maintain.append(sensor['name'])
    return sensors_to_maintain

# Шаг 3: Визуализация местоположения датчиков на карте
def visualize_sensors_on_map(sensor_data):
    m = folium.Map(location=[43.2609, 70.0122], zoom_start=13)

    for sensor in sensor_data:
        if sensor['status'] == 'working':
            folium.Marker([sensor['location'][0], sensor['location'][1]], popup=sensor['name'], icon=folium.Icon(color='green')).add_to(m)
        else:
            folium.Marker([sensor['location'][0], sensor['location'][1]], popup=sensor['name'], icon=folium.Icon(color='red')).add_to(m)

    m.save("146.html")

# Шаг 4: Вывод списка датчиков, требующих технического обслуживания
def print_sensors_to_maintain(sensors_to_maintain):
    if sensors_to_maintain:
        print(f"Датчики, требующие технического обслуживания: {', '.join(sensors_to_maintain)}")
    else:
        print("Все датчики работают нормально.")

# Основная часть кода
if __name__ == "__main__":
    sensor_data = get_sensor_data()
    sensors_to_maintain = check_sensor_status(sensor_data)
    visualize_sensors_on_map(sensor_data)
    print_sensors_to_maintain(sensors_to_maintain)