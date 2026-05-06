import folium

def get_river_water_levels():
    """
    Имитация функции получения данных из API гидрологической службы.
    В реальном сценарии здесь был бы запрос requests.get(url).
    """
    # Данные: Название, Координаты [lat, lon], Текущий уровень (м), Дата замера
    mock_api_response = [
        {
            "river": "Ili River",
            "coords": [43.5000, 79.5000], 
            "level": 12.45, 
            "unit": "m",
            "status": "Normal"
        },
        {
            "river": "Karatal River",
            "coords": [43.8000, 78.5000], 
            "level": 4.12, 
            "unit": "m",
            "status": "Low"
        }
    ]
    return mock_api_response

def create_hydrology_map(data):
    # Создаем карту, центрированную в регионе рек Или и Каратал (Казахстан)
    m = folium.Map(location=[43.65, 79.0], zoom_start=7, tiles='OpenStreetMap')

    # Цвета в зависимости от статуса уровня воды
    color_map = {
        "Normal": "blue",
        "Low": "orange",
        "High": "red"
    }

    for entry in data:
        # Создаем текст для всплывающего окна
        popup_text = f"<b>Река:</b> {entry['river']}<br>" \
                     f"<b>Уровень воды:</b> {entry['level']} {entry['unit']}<br>" \
                     f"<b>Статус:</b> {entry['status']}"
        
        # Добавляем маркер на карту
        folium.Marker(
            location=entry['coords'],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"Уровень воды: {entry['river']}",
            icon=folium.Icon(color=color_map.get(entry['status'], "gray"), icon="info-sign")
        ).add_to(m)

    # Сохранение карты строго в файл 9.html
    m.save("9.html")
    print("Карта успешно сохранена в файл 9.html")

if __name__ == "__main__":
    # 1. Получаем данные
    river_levels = get_river_water_levels()
    
    # 2. Визуализируем данные на карте
    create_hydrology_map(river_levels)