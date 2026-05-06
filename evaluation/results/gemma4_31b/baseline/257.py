import folium
import pandas as pd
import numpy as np

def calculate_irrigation_deficit(river_level, area_ha, crop_norm, critical_level=2.5):
    """
    Расчет дефицита воды для полива.
    :param river_level: Текущий уровень воды в реке (м)
    :param area_ha: Площадь участка (га)
    :param crop_norm: Норма полива (м3/га)
    :param critical_level: Критический уровень реки (м)
    :return: Объем необходимого полива (м3) и статус
    """
    # Модель доступности воды: чем выше уровень над критическим, тем больше воды доступно
    # Допустим, при уровне 5м доступность 100%, при critical_level доступность 0%
    max_capacity = area_ha * crop_norm
    availability_factor = np.clip((river_level - critical_level) / (5.0 - critical_level), 0, 1)
    
    available_water = max_capacity * availability_factor
    deficit = max(0, max_capacity - available_water)
    
    # Определение статуса
    if deficit == 0:
        status = "Достаточно"
        color = "green"
    elif deficit < max_capacity * 0.5:
        status = "Умеренный дефицит"
        color = "orange"
    else:
        status = "Критический дефицит"
        color = "red"
        
    return deficit, status, color

# --- Исходные данные ---
# Текущий уровень воды в реке Баянколь (м)
current_river_level = 3.2 
critical_threshold = 2.5

# Данные по сельскохозяйственным участкам (Координаты, Площадь, Норма полива)
plots_data = [
    {"id": "Участок 1", "lat": 44.512, "lon": 62.123, "area": 150, "norm": 450},
    {"id": "Участок 2", "lat": 44.530, "lon": 62.150, "area": 200, "norm": 500},
    {"id": "Участок 3", "lat": 44.490, "lon": 62.110, "area": 100, "norm": 400},
    {"id": "Участок 4", "lat": 44.550, "lon": 62.180, "area": 300, "norm": 600},
]

# Координаты реки Баянколь (примерная точка замера)
river_gauge_coords = [44.520, 62.135]

# --- Создание карты ---
m = folium.Map(location=river_gauge_coords, zoom_start=12, tiles="OpenStreetMap")

# Добавляем маркер уровня реки
folium.Marker(
    location=river_gauge_coords,
    popup=f"Уровень реки Баянколь: {current_river_level}м",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Расчет и добавление участков на карту
for plot in plots_data:
    deficit, status, color = calculate_irrigation_deficit(
        current_river_level, plot["area"], plot["norm"], critical_threshold
    )
    
    folium.CircleMarker(
        location=[plot["lat"], plot["lon"]],
        radius=10,
        popup=f"<b>{plot['id']}</b><br>Статус: {status}<br>Дефицит: {deficit:.2f} м³",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("257.html")

print("Расчет завершен. Карта сохранена в файл 257.html")