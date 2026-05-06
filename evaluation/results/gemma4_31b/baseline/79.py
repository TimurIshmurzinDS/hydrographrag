import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных по расходу воды для реки Turgen River
# В реальном сценарии здесь будет загрузка CSV или запрос к API гидрологической службы
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
# Создаем сезонный цикл: низкий расход зимой, пик весной (таяние снегов), умеренный летом
base_flow = 10 + 5 * np.sin(np.linspace(0, 2 * np.pi, len(dates)) - np.pi/2)
noise = np.random.normal(0, 2, len(dates))
discharge = base_flow + noise

# Искусственно создаем паводковый период в мае-июне
discharge[120:150] += 15 

df = pd.DataFrame({'date': dates, 'discharge': discharge})

# 2. Анализ признаков паводка
mean_flow = df['discharge'].mean()
std_flow = df['discharge'].std()
flood_threshold = mean_flow + 2 * std_flow  # Порог: среднее + 2 стандартных отклонения

# Проверка последних данных (имитируем текущую дату как конец июня)
current_discharge = df.iloc[-1]['discharge'] 
# Для демонстрации проверим период с 120 по 150 день
flood_detected = any(df['discharge'] > flood_threshold)
flood_periods = df[df['discharge'] > flood_threshold]

print(f"Средний расход: {mean_flow:.2f} м3/с")
print(f"Порог паводка: {flood_threshold:.2f} м3/с")
print(f"Признаки паводка обнаружены: {'Да' if flood_detected else 'Нет'}")

# 3. Геопространственная визуализация
# Координаты Turgen River (примерные координаты региона Алматинской области, Казахстан)
river_coords = [
    [43.120, 78.500], [43.130, 78.520], [43.150, 78.550], 
    [43.170, 78.580], [43.200, 78.610]
]
station_coord = [43.150, 78.550]

# Создание карты
m = folium.Map(location=[43.150, 78.550], zoom_start=11, tiles='OpenStreetMap')

# Цвет линии реки в зависимости от наличия паводка
line_color = 'red' if flood_detected else 'blue'
line_weight = 5 if flood_detected else 3

# Добавление русла реки на карту
folium.PolyLine(
    locations=river_coords, 
    color=line_color, 
    weight=line_weight, 
    tooltip="Turgen River"
).add_to(m)

# Добавление маркера гидропоста
status_text = "ВНИМАНИЕ: Признаки паводка!" if flood_detected else "Режим в норме"
folium.Marker(
    location=station_coord,
    popup=f"Гидропост Turgen River\nСтатус: {status_text}\nТекущий расход: {current_discharge:.2f} м3/с",
    icon=folium.Icon(color='red' if flood_detected else 'green', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("79.html")

print("Результат визуализации сохранен в файл 79.html")