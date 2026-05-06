import folium

# Пример данных о сенсорах: координаты и статус (True - активен, False - неактивен)
sensors = [
    {'name': 'Sensor 1', 'coordinates': [52.3456, 48.7890], 'active': True},
    {'name': 'Sensor 2', 'coordinates': [52.3567, 48.7901], 'active': False},
    {'name': 'Sensor 3', 'coordinates': [52.3678, 48.7912], 'active': True},
    {'name': 'Sensor 4', 'coordinates': [52.3789, 48.7923], 'active': False}
]

# Создание карты с центром в средней точке всех сенсоров
center_lat = sum(sensor['coordinates'][0] for sensor in sensors) / len(sensors)
center_lon = sum(sensor['coordinates'][1] for sensor in sensors) / len(sensors)

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Добавление маркеров на карту
for sensor in sensors:
    if sensor['active']:
        color = 'green'
    else:
        color = 'red'
    
    folium.Marker(
        location=sensor['coordinates'],
        popup=f"{sensor['name']} - {'Активен' if sensor['active'] else 'Неактивен'}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты в файл
m.save("71.html")