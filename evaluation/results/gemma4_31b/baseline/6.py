import folium

def solve_sensor_status():
    # 1. Имитация базы данных геосенсоров
    # В реальном проекте здесь был бы запрос к PostGIS или загрузка GeoJSON/Shapefile
    sensors_db = [
        {
            "sensor_id": "SN-001",
            "river_name": "Kumbel River",
            "lat": 42.3512, 
            "lon": 76.1234, 
            "status": "Active",
            "last_update": "2023-10-27 10:00"
        },
        {
            "sensor_id": "SN-002",
            "river_name": "Amudarya River",
            "lat": 41.1234, 
            "lon": 63.4567, 
            "status": "Inactive",
            "last_update": "2023-10-26 15:30"
        },
        {
            "sensor_id": "SN-003",
            "river_name": "Syr Darya",
            "lat": 43.5678, 
            "lon": 68.9101, 
            "status": "Maintenance",
            "last_update": "2023-10-27 08:15"
        }
    ]

    target_river = "Kumbel River"
    sensor_info = None

    # 2. Поиск сенсора на указанной реке
    for sensor in sensors_db:
        if sensor["river_name"] == target_river:
            sensor_info = sensor
            break

    if not sensor_info:
        print(f"Сенсор на реке {target_river} не найден.")
        return

    # 3. Вывод статуса в консоль
    status = sensor_info["status"]
    print(f"Статус сенсора на реке {target_river}: {status}")

    # 4. Визуализация на карте
    # Определяем цвет маркера в зависимости от статуса
    color_map = {
        "Active": "green",
        "Inactive": "red",
        "Maintenance": "orange"
    }
    marker_color = color_map.get(status, "blue")

    # Создание карты, центрированной на сенсоре
    m = folium.Map(location=[sensor_info["lat"], sensor_info["lon"]], zoom_start=12)

    # Добавление маркера с информацией
    popup_text = (f"Sensor ID: {sensor_info['sensor_id']}<br>"
                  f"River: {sensor_info['river_name']}<br>"
                  f"Status: {status}<br>"
                  f"Last Update: {sensor_info['last_update']}")
    
    folium.Marker(
        location=[sensor_info["lat"], sensor_info["lon"]],
        popup=popup_text,
        tooltip="Click for status",
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(m)

    # Сохранение карты строго в файл 6.html
    m.save("6.html")
    print("Карта успешно сохранена в файл 6.html")

if __name__ == "__main__":
    solve_sensor_status()