import folium
import random
from datetime import datetime

def get_water_sensor_data():
    """
    Симуляция получения данных с датчика уровня воды на реке Karatal.
    В реальном сценарии здесь будет запрос к REST API гидрологической службы.
    """
    # Координаты датчика на р. Karatal (примерные координаты региона)
    sensor_coords = [43.4521, 78.1234] 
    
    # Симуляция возможных состояний
    statuses = ["Online", "Online", "Online", "Offline"]
    current_status = random.choice(statuses)
    
    # Симуляция уровня воды в метрах
    water_level = round(random.uniform(1.2, 5.5), 2) if current_status == "Online" else None
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "coords": sensor_coords,
        "level": water_level,
        "status": current_status,
        "timestamp": timestamp
    }

def analyze_sensor_status(data):
    """
    Анализ данных датчика и определение цветового кода для карты.
    """
    threshold_critical = 4.5  # Порог критического уровня воды
    threshold_warning = 3.0   # Порог предупреждения
    
    if data["status"] == "Offline":
        return "Критический (Связь потеряна)", "red"
    
    if data["level"] >= threshold_critical:
        return f"Критический уровень: {data['level']}м", "red"
    elif data["level"] >= threshold_warning:
        return f"Предупреждение: {data['level']}м", "orange"
    else:
        return f"Норма: {data['level']}м", "green"

def main():
    # 1. Получаем данные с датчика
    sensor_data = get_water_sensor_data()
    
    # 2. Анализируем статус
    status_text, color = analyze_sensor_status(sensor_data)
    
    # 3. Создаем карту, центрированную на датчике
    m = folium.Map(location=sensor_data["coords"], zoom_start=12, control_scale=True)
    
    # 4. Формируем текст для всплывающего окна
    popup_info = (
        f"<b>Датчик: Karatal River Station</b><br>"
        f"Статус: {sensor_data['status']}<br>"
        f"Уровень воды: {sensor_data['level'] if sensor_data['level'] else 'N/A'} м<br>"
        f"Состояние: {status_text}<br>"
        f"Обновлено: {sensor_data['timestamp']}"
    )
    
    # 5. Добавляем маркер на карту
    folium.Marker(
        location=sensor_data["coords"],
        popup=folium.Popup(popup_info, max_width=300),
        tooltip="Проверить статус датчика",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)
    
    # 6. Сохранение карты
    m.save("2.html")
    print(f"Анализ завершен. Статус: {status_text}. Карта сохранена в 2.html")

if __name__ == "__main__":
    main()