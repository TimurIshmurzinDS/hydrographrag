import folium
import random

def check_water_alerts():
    # 1. Имитация пространственных данных реки Shyzhyn River
    # Координаты русла (упрощенно)
    river_coords = [
        [48.500, 35.100], [48.510, 35.120], [48.525, 35.150], 
        [48.540, 35.180], [48.560, 35.210], [48.580, 35.250]
    ]

    # 2. Данные гидрологических станций (ID, Координаты, Текущий уровень, Порог)
    # В реальном сценарии эти данные приходят из API (например, USGS или Copernicus)
    stations_data = [
        {"id": "ST_01", "coords": [48.510, 35.120], "current_level": 2.1, "threshold": 3.0},
        {"id": "ST_02", "coords": [48.540, 35.180], "current_level": 4.5, "threshold": 4.0}, # Превышение
        {"id": "ST_03", "coords": [48.580, 35.250], "current_level": 1.8, "threshold": 3.0},
    ]

    # Создание карты, центрированной на реке
    m = folium.Map(location=[48.540, 35.170], zoom_start=12, tiles="CartoDB positron")

    # Отрисовка русла реки
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.7, tooltip="Shyzhyn River").add_to(m)

    alerts_found = False

    # 3. Анализ и визуализация станций
    for station in stations_data:
        level = station["current_level"]
        threshold = station["threshold"]
        is_alert = level >= threshold
        
        if is_alert:
            alerts_found = True
            color = "red"
            status = "⚠️ ВЫСОКИЙ УРОВЕНЬ!"
        else:
            color = "green"
            status = "Норма"

        # Добавление маркера станции на карту
        folium.CircleMarker(
            location=station["coords"],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Станция: {station['id']}<br>Уровень: {level}м<br>Порог: {threshold}м<br>Статус: {status}"
        ).add_to(m)

    # Добавление общего текстового уведомления на карту
    if alerts_found:
        alert_text = "ВНИМАНИЕ: Обнаружены оповещения о высоком уровне воды на реке Shyzhyn River!"
    else:
        alert_text = "Оповещений о высоком уровне воды для реки Shyzhyn River не обнаружено."
    
    # Добавляем заголовок через HTML-элемент
    title_html = f'''
       <div style="position: fixed; 
                   top: 50px; left: 50px; width: 300px; height: 90px; 
                   z-index: 9999; font-size: 14px; 
                   background-color: white; 
                   padding: 10px; 
                   border: 2px solid black;
                   border-radius: 10px;">
       <b>Мониторинг Shyzhyn River</b><br>{alert_text}
       </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Сохранение карты
    m.save("28.html")
    print("Анализ завершен. Карта сохранена в файл 28.html")
    return alerts_found

if __name__ == "__main__":
    has_alerts = check_water_alerts()
    if has_alerts:
        print("Результат: Есть оповещения о высоком уровне воды.")
    else:
        print("Результат: Оповещений нет.")