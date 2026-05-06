import folium
import random

def get_current_water_level(river_name):
    """
    Имитация функции получения данных из API гидрологической службы.
    В реальном сценарии здесь был бы запрос requests.get(api_url).
    """
    # Предположим, нормальный уровень реки - 2.5 метра
    # Генерируем случайное значение для демонстрации разных статусов
    levels = [1.8, 2.5, 3.2, 4.5] # Низкий, Норма, Предупреждение, Опасность
    return random.choice(levels)

def get_status_and_color(level):
    """
    Определяет статус уровня воды и соответствующий цвет маркера.
    """
    if level < 2.0:
        return "Низкий уровень", "blue"
    elif 2.0 <= level < 3.0:
        return "Норма", "green"
    elif 3.0 <= level < 4.0:
        return "Предупреждение", "orange"
    else:
        return "Опасность (Паводок)", "red"

def main():
    # 1. Параметры реки и станции
    river_name = "Prokhodnaya River"
    # Координаты (примерные координаты для демонстрации)
    station_coords = [56.45, 60.12] 
    
    # 2. Получение данных
    current_level = get_current_water_level(river_name)
    status, color = get_status_and_color(current_level)
    
    print(f"Река: {river_name}")
    print(f"Текущий уровень: {current_level} м.")
    print(f"Статус: {status}")

    # 3. Создание карты
    # Центрируем карту на координатах станции
    m = folium.Map(location=station_coords, zoom_start=12, tiles='OpenStreetMap')

    # 4. Добавление маркера гидропоста
    popup_text = f"""
    <b>Река:</b> {river_name}<br>
    <b>Текущий уровень:</b> {current_level} м.<br>
    <b>Статус:</b> {status}
    """
    
    folium.Marker(
        location=station_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Гидропост Prokhodnaya River",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

    # 5. Сохранение карты
    m.save("5.html")
    print("Карта успешно сохранена в файл 5.html")

if __name__ == "__main__":
    main()