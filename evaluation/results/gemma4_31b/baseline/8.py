import folium
import random
from datetime import datetime

def get_sensor_status():
    """
    Симуляция получения данных с датчика мониторинга реки Ulken Almaty.
    В реальном сценарии здесь был бы запрос к REST API или базе данных.
    """
    statuses = ["Online", "Offline"]
    # Имитируем случайное состояние датчика
    current_status = random.choice(statuses)
    
    # Имитируем уровень воды в метрах
    water_level = round(random.uniform(0.5, 3.5), 2) if current_status == "Online" else None
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "sensor_id": "UA-RIVER-001",
        "status": current_status,
        "water_level": water_level,
        "timestamp": timestamp,
        "coords": [43.225, 76.912]  # Примерные координаты в районе реки Ulken Almaty
    }

def main():
    # 1. Получаем данные о состоянии датчика
    data = get_sensor_status()
    lat, lon = data["coords"]
    
    # 2. Определяем цвет маркера и текстовое сообщение на основе статуса
    if data["status"] == "Online":
        marker_color = "green"
        status_text = f"✅ Состояние: Работает<br>Уровень воды: {data['water_level']} м<br>Обновлено: {data['timestamp']}"
    else:
        marker_color = "red"
        status_text = f"❌ Состояние: ОФЛАЙН<br>Данные недоступны<br>Последняя проверка: {data['timestamp']}"

    # 3. Создание карты
    # Центрируем карту на координатах датчика
    m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)

    # 4. Добавление маркера датчика на карту
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(status_text, max_width=300),
        tooltip="Датчик мониторинга Ulken Almaty River",
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(m)

    # Добавление подписи к карте
    folium.map.Marker([lat, lon], 
                     icon=folium.DivIcon(html=f'<div style="font-family: Arial; color: black; font-weight: bold; width: 200px;">Река Ulken Almaty: {data["status"]}</div>')).add_to(m)

    # 5. Сохранение карты в файл 8.html
    m.save("8.html")
    print(f"Анализ завершен. Статус датчика: {data['status']}. Карта сохранена в 8.html")

if __name__ == "__main__":
    main()