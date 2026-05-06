import folium
import random

def simulate_karaoy_river_teleportation():
    # 1. Координаты сенсоров вдоль реки Karaoy (симуляция расположения)
    # Приблизительные координаты региона
    sensors_data = [
        {"id": "Sensor_1", "coords": [44.123, 70.456], "value": random.uniform(0, 10)},
        {"id": "Sensor_2", "coords": [44.150, 70.510], "value": random.uniform(0, 10)},
        {"id": "Sensor_3", "coords": [44.180, 70.580], "value": random.uniform(0, 10)},
        {"id": "Sensor_4", "coords": [44.210, 70.650], "value": random.uniform(0, 10)},
        {"id": "Sensor_5", "coords": [44.250, 70.720], "value": random.uniform(0, 10)},
    ]

    # Начальная точка наблюдателя (Базовая станция)
    start_point = [44.100, 70.400]
    
    # 2. Логика определения цели для телепортации
    # Телепортируемся к сенсору с максимальным значением (например, уровень паводка)
    target_sensor = max(sensors_data, key=lambda x: x['value'])
    target_coords = target_sensor['coords']
    
    print(f"Критический уровень обнаружен на {target_sensor['id']}!")
    print(f"Инициирую телепортацию из {start_point} в {target_coords}...")

    # 3. Создание карты
    # Центрируем карту вокруг области реки
    m = folium.Map(location=[44.175, 70.580], zoom_start=11, tiles="CartoDB positron")

    # Добавляем начальную точку
    folium.Marker(
        location=start_point, 
        popup="Начальная точка (База)", 
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(m)

    # Добавляем все сенсоры на карту
    for sensor in sensors_data:
        color = 'green' if sensor['value'] < 7 else 'red'
        folium.CircleMarker(
            location=sensor['coords'],
            radius=8,
            popup=f"{sensor['id']} - Значение: {sensor['value']:.2f}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # 4. Визуализация "Телепортации"
    # Рисуем линию прыжка (пунктирная линия от старта к цели)
    folium.PolyLine(
        locations=[start_point, target_coords],
        color='purple',
        weight=5,
        opacity=0.7,
        dash_array='10',
        tooltip="Путь телепортации"
    ).add_to(m)

    # Маркер целевого сенсора (куда телепортировались)
    folium.Marker(
        location=target_coords,
        popup=f"ЦЕЛЬ ТЕЛЕПОРТАЦИИ: {target_sensor['id']}",
        icon=folium.Icon(color='purple', icon='bolt')
    ).add_to(m)

    # Сохранение карты
    m.save("216.html")
    print("Карта успешно сохранена в файл 216.html")

if __name__ == "__main__":
    simulate_karaoy_river_teleportation()