import folium
import requests
import random

def get_ili_river_water_level():
    """
    Имитация функции получения данных из API гидрологической службы.
    В реальном сценарии здесь будет запрос к REST API или базе данных.
    """
    # Координаты репрезентативной точки на реке Или (например, в районе впадения в оз. Балхаш)
    station_coords = [43.85, 78.50] 
    station_name = "Гидропост Или-Балхаш"
    
    # Имитация получения данных (в метрах)
    # В реальности: response = requests.get(api_url).json()
    current_level = round(random.uniform(2.5, 4.8), 2) 
    status = "Норма" if 3.0 <= current_level <= 4.0 else "Отклонение"
    
    return {
        "coords": station_coords,
        "name": station_name,
        "level": current_level,
        "status": status
    }

def main():
    # 1. Получаем данные о уровне воды
    data = get_ili_river_water_level()
    
    # 2. Инициализируем карту, центрируя её на координатах станции
    m = folium.Map(location=data['coords'], zoom_start=7, tiles='OpenStreetMap')
    
    # 3. Создаем информационное сообщение для маркера
    popup_text = f"""
    <b>Станция:</b> {data['name']}<br>
    <b>Текущий уровень воды:</b> {data['level']} м.<br>
    <b>Статус:</b> {data['status']}<br>
    <i>Данные обновлены в реальном времени (симуляция)</i>
    """
    
    # 4. Добавляем маркер на карту
    folium.Marker(
        location=data['coords'],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Нажмите для просмотра уровня воды",
        icon=folium.Icon(color='blue', icon='tint')
    ).add_to(m)
    
    # Дополнительно: Добавим линию, имитирующую русло реки в данной области
    # (Упрощенно: линия от Китая к Балхашу)
    river_path = [
        [43.2, 76.0], [43.5, 77.0], [43.8, 78.0], [43.85, 78.5]
    ]
    folium.PolyLine(river_path, color="blue", weight=4, opacity=0.7, tooltip="Русло реки Или").add_to(m)

    # 5. Сохранение карты в файл 1.html
    m.save("1.html")
    print("Карта успешно создана и сохранена в файл 1.html")
    print(f"Текущий уровень воды в реке Или: {data['level']} м.")

if __name__ == "__main__":
    main()