import folium
import random
from datetime import datetime

def get_river_water_level():
    """
    Симуляция получения данных из API гидрологического мониторинга.
    В реальном сценарии здесь будет запрос к REST API (например, через requests).
    """
    # Координаты реки Osek (примерные координаты для региона)
    coords = [50.65, 13.65] 
    
    # Симуляция текущего уровня воды в метрах
    # В период паводка значения обычно выше нормы
    current_level = round(random.uniform(1.5, 5.5), 2) 
    
    # Пороговые значения
    thresholds = {
        "warning": 3.0,
        "danger": 4.5
    }
    
    # Определение статуса и цвета
    if current_level >= thresholds["danger"]:
        status = "КРИТИЧЕСКИЙ (Паводок)"
        color = "red"
    elif current_level >= thresholds["warning"]:
        status = "ПРЕДУПРЕЖДЕНИЕ"
        color = "orange"
    else:
        status = "НОРМА"
        color = "green"
        
    return {
        "coords": coords,
        "level": current_level,
        "status": status,
        "color": color,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    # 1. Получаем данные
    data = get_river_water_level()
    
    # 2. Инициализируем карту вокруг координат реки
    m = folium.Map(location=data["coords"], zoom_start=12, control_scale=True)
    
    # 3. Создаем информационное сообщение для всплывающего окна
    popup_text = (
        f"<b>Река: Osek River</b><br>"
        f"Текущий уровень: {data['level']} м<br>"
        f"Статус: {data['status']}<br>"
        f"Время замера: {data['time']}"
    )
    
    # 4. Добавляем маркер на карту
    folium.Marker(
        location=data["coords"],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip="Гидрологический пост Osek River",
        icon=folium.Icon(color=data["color"], icon="info-sign")
    ).add_to(m)
    
    # Дополнительно: Добавляем круг влияния (зону возможного разлива при паводке)
    if data["color"] == "red":
        folium.Circle(
            location=data["coords"],
            radius=2000, # 2 км зона риска
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.2,
            popup="Зона возможного затопления"
        ).add_to(m)

    # 5. Сохранение карты
    m.save("26.html")
    print(f"Анализ завершен. Статус: {data['status']}. Карта сохранена в 26.html")

if __name__ == "__main__":
    main()