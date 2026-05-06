import folium
import random

def get_current_water_level(river_name):
    """
    Симуляция запроса к API гидрологического мониторинга.
    В реальном сценарии здесь будет запрос к REST API (например, requests.get(url)).
    """
    # Имитация данных: уровень воды в метрах
    # Для Большого Алматы предполагаем диапазон от 0.5 до 3.0 метров
    mock_data = {
        "river": river_name,
        "current_level": round(random.uniform(0.8, 2.5), 2),
        "unit": "meters",
        "status": "Normal"
    }
    
    # Определение статуса на основе уровня
    if mock_data["current_level"] > 2.0:
        mock_data["status"] = "Warning (High Level)"
    elif mock_data["current_level"] < 1.0:
        mock_data["status"] = "Low Level"
        
    return mock_data

def main():
    # 1. Координаты реки Большой Алматы (приблизительный центр/гидропост)
    # Координаты в районе предгорий Алматы
    river_coords = [43.1500, 76.9000] 
    station_coords = [43.1620, 76.8850]
    
    # Линия русла (упрощенно для визуализации)
    river_path = [
        [43.1800, 76.8600],
        [43.1620, 76.8850],
        [43.1500, 76.9000],
        [43.1300, 76.9200]
    ]

    # 2. Получение данных
    data = get_current_water_level("Ulken Almaty River")
    level = data["current_level"]
    status = data["status"]

    # 3. Определение цвета маркера в зависимости от статуса
    color = "green" if status == "Normal" else "orange" if status == "Low Level" else "red"

    # 4. Создание карты
    m = folium.Map(location=river_coords, zoom_start=12, control_scale=True)

    # Добавление линии реки
    folium.PolyLine(
        locations=river_path,
        color="blue",
        weight=5,
        opacity=0.7,
        tooltip="Ulken Almaty River"
    ).add_to(m)

    # Добавление маркера гидропоста
    folium.Marker(
        location=station_coords,
        popup=f"<b>Station: Ulken Almaty</b><br>Current Level: {level}m<br>Status: {status}",
        tooltip="Water Level Sensor",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

    # Добавление текстового уведомления на карту
    folium.Popup(f"Current water level in Ulken Almaty River: {level}m ({status})").add_to(m)

    # Сохранение карты
    m.save("15.html")
    print(f"Modeling complete. Current level: {level}m. Map saved as 15.html")

if __name__ == "__main__":
    main()