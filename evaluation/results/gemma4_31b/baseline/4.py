import folium
import random
from datetime import datetime, timedelta

def get_station_status(station_id):
    """
    Симуляция запроса к API станции мониторинга.
    В реальном проекте здесь был бы запрос requests.get(api_url)
    """
    statuses = ["Active", "Inactive", "Maintenance"]
    # Симулируем случайный статус для демонстрации работы модели
    status = random.choice(statuses)
    last_update = datetime.now() - timedelta(minutes=random.randint(0, 120))
    value = round(random.uniform(1.2, 5.8), 2) # Симуляция уровня воды в метрах
    
    return {
        "id": station_id,
        "status": status,
        "last_update": last_update.strftime("%Y-%m-%d %H:%M:%S"),
        "water_level": value
    }

def main():
    # 1. Координаты реки Koktal (примерные координаты для региона)
    # В реальности используются точные координаты из ГИС-слоя
    koktal_river_coords = [42.35, 72.10] 
    station_coords = [42.36, 72.12]
    station_id = "KOKTAL_MON_01"

    # 2. Получение данных о состоянии станции
    data = get_station_status(station_id)
    status = data['status']
    
    # Определяем, работает ли станция сейчас
    # Считаем работающей только если статус 'Active'
    is_working = True if status == "Active" else False
    
    # 3. Визуализация
    # Создаем карту, центрированную на реке
    m = folium.Map(location=koktal_river_coords, zoom_start=12, tiles='OpenStreetMap')

    # Определяем цвет маркера в зависимости от статуса
    marker_color = 'green' if is_working else 'red'
    status_text = "РАБОТАЕТ" if is_working else "НЕ РАБОТАЕТ / ОШИБКА"

    # Создаем текст для всплывающего окна
    popup_info = (
        f"<b>Станция:</b> {data['id']}<br>"
        f"<b>Статус:</b> {status_text} ({status})<br>"
        f"<b>Уровень воды:</b> {data['water_level']} м.<br>"
        f"<b>Последнее обновление:</b> {data['last_update']}"
    )

    # Добавляем маркер станции на карту
    folium.Marker(
        location=station_coords,
        popup=folium.Popup(popup_info, max_width=300),
        tooltip="Станция мониторинга Koktal River",
        icon=folium.Icon(color=marker_color, icon='info-sign')
    ).add_to(m)

    # Добавляем линию, имитирующую русло реки для контекста
    river_line = [
        [42.30, 72.05],
        [42.33, 72.08],
        [42.36, 72.12],
        [42.40, 72.15]
    ]
    folium.PolyLine(river_line, color="blue", weight=5, opacity=0.7, tooltip="Koktal River").add_to(m)

    # Сохранение карты
    m.save("4.html")
    print(f"Анализ завершен. Статус станции {station_id}: {status_text}. Карта сохранена в 4.html")

if __name__ == "__main__":
    main()