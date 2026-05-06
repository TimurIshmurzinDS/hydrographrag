import folium

# Предполагаемые данные о сенсорах (в реальности данные могут быть получены из базы данных или API)
sensors_data = [
    {
        "name": "Sensor_1",
        "location": [46.5833, 7.9000],  # Координаты примерные
        "status": "активен"            # Статус сенсора
    },
    {
        "name": "Sensor_2",
        "location": [46.5900, 7.8900],
        "status": "неактивен"
    }
]

# Создание карты folium
m = folium.Map(location=[46.5833, 7.9000], zoom_start=12)

# Добавление маркеров на карту для каждого сенсора
for sensor in sensors_data:
    if sensor["name"] == "Sensor_1":  # Предполагаем, что Sensor_1 находится на реке Kumbel River
        folium.Marker(
            location=sensor["location"],
            popup=f"Сенсор: {sensor['name']}\nСтатус: {sensor['status']}",
            icon=folium.Icon(color='green' if sensor['status'] == 'активен' else 'red')
        ).add_to(m)

# Сохранение карты в файл
m.save("6.html")