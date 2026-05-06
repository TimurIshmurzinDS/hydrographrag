import folium

def solve_gis_task():
    # 1. Симуляция данных об оборудовании на реке Temirlik
    # Координаты подобраны приблизительно для региона реки Temirlik (Казахстан)
    equipment_data = [
        {"id": "SEN_01", "lat": 43.2512, "lon": 76.9123, "type": "Уровень воды", "status": "Working"},
        {"id": "SEN_02", "lat": 43.2650, "lon": 76.9345, "type": "Качество воды", "status": "Faulty"},
        {"id": "SEN_03", "lat": 43.2810, "lon": 76.9510, "type": "Гидропост", "status": "Working"},
        {"id": "SEN_04", "lat": 43.2950, "lon": 76.9720, "type": "Уровень воды", "status": "Faulty"},
        {"id": "SEN_05", "lat": 43.3100, "lon": 76.9980, "type": "Качество воды", "status": "Working"},
    ]

    # 2. Аппроксимация русла реки (линия по точкам)
    river_path = [
        [43.2400, 76.8900],
        [43.2512, 76.9123],
        [43.2650, 76.9345],
        [43.2810, 76.9510],
        [43.2950, 76.9720],
        [43.3100, 76.9980],
        [43.3250, 77.0200],
    ]

    # Создание карты, центрированной на среднем значении координат
    m = folium.Map(location=[43.27, 76.95], zoom_start=12, tiles='OpenStreetMap')

    # 3. Отрисовка русла реки
    folium.PolyLine(
        locations=river_path, 
        color='blue', 
        weight=5, 
        opacity=0.7, 
        tooltip="Река Temirlik"
    ).add_to(m)

    # 4. Добавление оборудования на карту с проверкой работоспособности
    for device in equipment_data:
        # Определяем цвет в зависимости от статуса
        color = 'green' if device['status'] == 'Working' else 'red'
        status_text = '✅ Работает' if device['status'] == 'Working' else '❌ НЕИСПРАВЕН'
        
        folium.CircleMarker(
            location=[device['lat'], device['lon']],
            radius=8,
            popup=f"ID: {device['id']}<br>Тип: {device['type']}<br>Статус: {status_text}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

    # Сохранение результата
    m.save("66.html")
    print("Карта успешно создана и сохранена в файл 66.html")

if __name__ == "__main__":
    solve_gis_task()