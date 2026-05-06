import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point, LineString

# 1. Имитация данных (так как реальные данные требуют доступа к ГИС-серверам Казахстана)
# Координаты реки Аягоз (приблизительные для демонстрации)
river_coords = [
    [48.8, 82.5], [48.7, 82.8], [48.6, 83.1], [48.5, 83.4], [48.4, 83.7]
]

# Данные по ирригационным зонам (Участки вдоль реки)
irrigation_data = {
    'zone_id': [1, 2, 3, 4],
    'lat': [48.75, 48.65, 48.55, 48.45],
    'lon': [82.6, 82.9, 83.2, 83.5],
    'area_ha': [1200, 2500, 1800, 3000], # Площадь в гектарах
    'water_need_m3_ha': [450, 500, 400, 550] # Потребность м3 на 1 га
}

df_irr = pd.DataFrame(irrigation_data)

# Параметры доступности воды в реке (упрощенно)
# Средний расход реки Аягоз (м3/с) за вегетационный период
avg_river_flow = 2.5 
# Общий доступный объем за сезон (м3) = расход * сек в сезоне * коэф. забора (0.4)
seconds_in_season = 90 * 24 * 3600 # 90 дней полива
total_supply_m3 = avg_river_flow * seconds_in_season * 0.4

# 2. Расчет дефицита
# Расчет потребности для каждой зоны
df_irr['total_demand_m3'] = df_irr['area_ha'] * df_irr['water_need_m3_ha']
total_demand_m3 = df_irr['total_demand_m3'].sum()

# Расчет общего дефицита
deficit_m3 = total_demand_m3 - total_supply_m3
deficit_percentage = (deficit_m3 / total_demand_m3) * 100 if total_demand_m3 > 0 else 0

print(f"Общий спрос на воду: {total_demand_m3:,.2f} м3")
print(f"Доступный объем воды: {total_supply_m3:,.2f} м3")
print(f"Абсолютный дефицит: {deficit_m3:,.2f} м3")
print(f"Уровень дефицита: {deficit_percentage:.2f}%")

# 3. Визуализация с помощью Folium
# Создаем карту, центрированную на регионе
m = folium.Map(location=[48.6, 83.0], zoom_start=8, tiles='OpenStreetMap')

# Рисуем реку Аягоз
folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.8, tooltip="Река Аягоз").add_to(m)

# Добавляем ирригационные зоны
for index, row in df_irr.iterrows():
    # Определяем цвет в зависимости от размера зоны (как прокси для нагрузки на реку)
    color = 'red' if deficit_percentage > 10 else 'orange' if deficit_percentage > 0 else 'green'
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['area_ha'] / 100, # Радиус зависит от площади
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Зона {row['zone_id']}<br>Площадь: {row['area_ha']} га<br>Спрос: {row['total_demand_m3']} м3"
    ).add_to(m)

# Добавляем легенду/информацию на карту
info_text = f"Анализ дефицита воды р. Аягоз<br>Общий дефицит: {deficit_percentage:.2f}%"
folium.Popup(info_text).add_to(m) # Simplified info

# Сохранение карты
m.save("35.html")