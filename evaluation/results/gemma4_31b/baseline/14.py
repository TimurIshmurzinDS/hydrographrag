import folium
import pandas as pd
import random

# 1. Симуляция данных системы мониторинга реки Batareyka
# Координаты подобраны условно для демонстрации геопространственного анализа
river_coords = [
    [53.450, 30.120], [53.455, 30.135], [53.462, 30.150], 
    [53.470, 30.160], [53.485, 30.175], [53.500, 30.190]
]

# Создаем список датчиков, расположенных вдоль реки
sensors_data = [
    {"id": "SN-01", "lat": 53.450, "lon": 30.120, "status": "Online", "value": 1.2},
    {"id": "SN-02", "lat": 53.455, "lon": 30.135, "status": "Online", "value": -0.5}, # Ошибка: отрицательное значение
    {"id": "SN-03", "lat": 53.462, "lon": 30.150, "status": "Offline", "value": None}, # Ошибка: оффлайн
    {"id": "SN-04", "lat": 53.470, "lon": 30.160, "status": "Online", "value": 1.1},
    {"id": "SN-05", "lat": 53.485, "lon": 30.175, "status": "Online", "value": 5.8}, # Ошибка: аномальный скачок
    {"id": "SN-06", "lat": 53.500, "lon": 30.190, "status": "Online", "value": 1.3},
]

def check_sensor_health(sensor):
    """Логика проверки работоспособности датчика"""
    if sensor["status"] == "Offline":
        return "Critical", "red"
    if sensor["value"] is None or sensor["value"] < 0 or sensor["value"] > 5.0:
        return "Warning", "orange"
    return "OK", "green"

# 2. Инициализация карты
m = folium.Map(location=[53.475, 30.155], zoom_start=13, tiles="CartoDB positron")

# 3. Отрисовка русла реки
folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.7, tooltip="Batareyka River").add_to(m)

# 4. Анализ и добавление датчиков на карту
working_count = 0
total_sensors = len(sensors_data)

for s in sensors_data:
    health_status, color = check_sensor_health(s)
    if health_status == "OK":
        working_count += 1
    
    # Создание всплывающего окна с информацией
    popup_text = (f"Sensor ID: {s['id']}<br>"
                  f"Status: {s['status']}<br>"
                  f"Value: {s['value']}m<br>"
                  f"Health: {health_status}")
    
    folium.CircleMarker(
        location=[s["lat"], s["lon"]],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=200)
    ).add_to(m)

# 5. Итоговый отчет в консоль
health_percentage = (working_count / total_sensors) * 100
print(f"--- Отчет по системе мониторинга Batareyka River ---")
print(f"Всего датчиков: {total_sensors}")
print(f"Исправных датчиков: {working_count}")
print(f"Общая работоспособность системы: {health_percentage:.2f}%")

# Сохранение карты
m.save("14.html")