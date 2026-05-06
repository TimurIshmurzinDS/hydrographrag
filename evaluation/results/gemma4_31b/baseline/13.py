import folium
import requests
from datetime import datetime

def get_water_level_data(river_name):
    """
    Имитация функции получения данных из API гидрологической службы.
    В реальном проекте здесь будет запрос к API (например, через requests.get).
    """
    # Мокап данных для реки Kumbel
    mock_api_response = {
        "river": "Kumbel River",
        "station_id": "KMB-001",
        "coordinates": [5.4500, 35.1200],  # Примерные координаты
        "water_level": 4.25,               # Уровень в метрах
        "unit": "m",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Normal"
    }
    
    if river_name.lower() == "kumbel river":
        return mock_api_response
    else:
        return None

def main():
    river_name = "Kumbel River"
    print(f"Запрос данных для {river_name}...")
    
    # 1. Получение данных
    data = get_water_level_data(river_name)
    
    if data:
        lat, lon = data['coordinates']
        level = data['water_level']
        unit = data['unit']
        time = data['timestamp']
        status = data['status']
        
        print(f"Последние показания: {level} {unit} (Статус: {status}) от {time}")
        
        # 2. Создание карты
        # Используем OpenStreetMap как базовый слой
        m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
        
        # 3. Создание информационного окна
        popup_text = f"""
        <b>Река:</b> {river_name}<br>
        <b>Станция:</b> {data['station_id']}<br>
        <b>Уровень воды:</b> {level} {unit}<br>
        <b>Статус:</b> {status}<br>
        <b>Дата замера:</b> {time}
        """
        
        # 4. Добавление маркера на карту
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip="Кликните для просмотра уровня воды",
            icon=folium.Icon(color='blue', icon='tint')
        ).add_to(m)
        
        # 5. Сохранение карты
        m.save("13.html")
        print("Карта успешно сохранена в файл 13.html")
    else:
        print("Данные для указанной реки не найдены.")

if __name__ == "__main__":
    main()