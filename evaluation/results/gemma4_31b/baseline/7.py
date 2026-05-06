import folium
import random
from datetime import datetime

def get_batareyka_water_level():
    """
    Симуляция получения данных с гидрологического датчика.
    В реальном сценарии здесь будет запрос к API (например, requests.get(url)).
    """
    # Имитация данных: уровень воды в метрах
    # Предположим, нормальный уровень 1.2м, текущий варьируется
    current_level = round(random.uniform(0.8, 2.5), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_level, timestamp

def main():
    # 1. Координаты реки Батарейка (примерные координаты для демонстрации)
    # Примечание: Точные координаты зависят от конкретного гидропоста
    river_coords = [48.4500, 39.2000] 
    river_name = "Batareyka River"

    # 2. Получение текущих данных
    water_level, time_updated = get_batareyka_water_level()
    
    # Определение статуса уровня воды
    if water_level < 1.0:
        status = "Низкий"
        color = "blue"
    elif 1.0 <= water_level <= 1.8:
        status = "Норма"
        color = "green"
    else:
        status = "Повышенный"
        color = "red"

    # 3. Создание карты
    # Центрируем карту на координатах реки
    m = folium.Map(location=river_coords, zoom_start=12, control_scale=True)

    # 4. Создание информационного текста для маркера
    popup_text = f"""
    <b>Река:</b> {river_name}<br>
    <b>Текущий уровень:</b> {water_level} м.<br>
    <b>Статус:</b> {status}<br>
    <b>Обновлено:</b> {time_updated}
    """

    # 5. Добавление маркера на карту
    folium.Marker(
        location=river_coords,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Станция мониторинга р. Батарейка",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

    # Добавление круга вокруг точки для визуализации зоны влияния
    folium.Circle(
        location=river_coords,
        radius=500,
        color=color,
        fill=True,
        fill_opacity=0.3
    ).add_to(m)

    # 6. Сохранение карты
    m.save("7.html")
    print(f"Данные успешно получены. Уровень воды: {water_level}м. Карта сохранена в 7.html")

if __name__ == "__main__":
    main()