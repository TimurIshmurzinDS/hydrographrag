import folium

# Пример данных о датчиках уровня воды (в реальности данные могут быть получены из API или базы данных)
sensor_data = [
    {"name": "Tentek River Sensor 1", "lat": 42.8743, "lon": 69.5011, "status": "Активен"},
    {"name": "Tentek River Sensor 2", "lat": 42.8750, "lon": 69.5020, "status": "Неактивен"},
    {"name": "Temirlik River Sensor 1", "lat": 43.2450, "lon": 69.1850, "status": "Активен"},
    {"name": "Temirlik River Sensor 2", "lat": 43.2460, "lon": 69.1860, "status": "Неактивен"}
]

# Создание карты
m = folium.Map(location=[43.0597, 69.2164], zoom_start=10)

# Добавление маркеров на карту
for sensor in sensor_data:
    folium.Marker(
        location=[sensor['lat'], sensor['lon']],
        popup=f"Датчик: {sensor['name']}\nСтатус: {sensor['status']}",
        icon=folium.Icon(color='green' if sensor['status'] == 'Активен' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("72.html")