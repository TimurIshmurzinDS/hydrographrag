import folium
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Имитация данных о расходе воды в реке Karatal (discharge data)
# Создаем временной ряд данных о расходе воды (м3/с)
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100)
discharge_values = np.random.normal(loc=15, scale=5, size=100) # Средний расход 15 м3/с
df_water = pd.DataFrame({'date': dates, 'discharge': discharge_values})

# Текущий показатель расхода воды (последнее значение)
current_discharge = df_water['discharge'].iloc[-1]
threshold_discharge = 10.0  # Порог: если < 10 м3/с, готовить суп нельзя (экологический лимит)

# 2. Геоданные реки Karatal (приблизительные координаты русла)
# Координаты для визуализации (упрощенная линия реки)
karatal_river_coords = [
    [43.12, 78.50], [43.15, 78.60], [43.20, 78.75], 
    [43.25, 78.90], [43.30, 79.10], [43.35, 79.30]
]

# Точка забора воды для супа (оптимальный участок)
soup_station_coords = [43.25, 78.90]

# 3. Логика "Приготовления супа"
if current_discharge >= threshold_discharge:
    soup_status = f"✅ Расход воды {current_discharge:.2f} м3/с. Воды достаточно. Можно готовить суп!"
    marker_color = "green"
else:
    soup_status = f"❌ Расход воды {current_discharge:.2f} м3/с. Слишком низкий уровень. Суп отменяется."
    marker_color = "red"

# 4. Визуализация с помощью folium
# Создаем карту, центрированную на реке Karatal
m = folium.Map(location=[43.22, 78.90], zoom_start=9, tiles="OpenStreetMap")

# Рисуем русло реки
folium.PolyLine(
    locations=karatal_river_coords, 
    color="blue", 
    weight=5, 
    opacity=0.8, 
    tooltip="Река Karatal"
).add_to(m)

# Добавляем точку "Soup Station"
folium.Marker(
    location=soup_station_coords,
    popup=folium.Popup(soup_status, max_width=300),
    tooltip="Точка приготовления супа",
    icon=folium.Icon(color=marker_color, icon="info-sign")
).add_to(m)

# Добавляем информационную панель (текст на карту через HTML)
html_content = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 300px; height: 100px; 
                background-color: white; border:2px solid black; z-index:9999; font-size:14px;
                padding: 10px; font-family: Arial, sans-serif;">
        <b>GIS Soup Model: Karatal River</b><br>
        Текущий расход: {current_discharge:.2f} м3/с<br>
        Статус: {soup_status}
    </div>
"""
m.get_root().html.add_child(folium.Element(html_content))

# Сохранение карты
m.save("214.html")

print("Modeling complete. The map has been saved as 214.html")
print(f"Current Status: {soup_status}")