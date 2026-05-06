import folium
from folium.plugins import MarkerCluster

# Пример данных: координаты и значения уровня воды для датчиков
sensor_data = {
    'Sensor1': {'lat': 55.7558, 'lon': 37.6173, 'level': 2.0},
    'Sensor2': {'lat': 55.7560, 'lon': 37.6175, 'level': 1.5},
    'Sensor3': {'lat': 55.7562, 'lon': 37.6177, 'level': 2.5}
}

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=14)

# Создание кластера маркеров для лучшей визуализации
marker_cluster = MarkerCluster().add_to(m)

# Определение порогов уровней воды
low_level_threshold = 2.0
high_level_threshold = 3.0

# Добавление маркеров на карту с соответствующим статусом
for sensor, data in sensor_data.items():
    lat, lon = data['lat'], data['lon']
    level = data['level']
    
    if level < low_level_threshold:
        color = 'red'
        status = 'Низкий уровень'
    elif level > high_level_threshold:
        color = 'green'
        status = 'Высокий уровень'
    else:
        color = 'yellow'
        status = 'Средний уровень'
    
    folium.Marker(
        [lat, lon],
        popup=f'{sensor}: {status} (Уровень: {level})',
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("136.html")