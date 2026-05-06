import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from shapely.geometry import LineString, Point

# 1. Симуляция данных (в реальном сценарии здесь будет загрузка из GeoJSON или SQL)
# Координаты реки Кумбель (условный отрезок для демонстрации)
river_coords = [
    [52.10, 63.50], [52.15, 63.60], [52.20, 63.75], 
    [52.25, 63.85], [52.30, 64.00], [52.35, 64.15]
]

# Создание синтетического набора данных по водозаборам АПК
np.random.seed(42)
num_points = 15
data = {
    'point_id': range(1, num_points + 1),
    'lat': np.interp(np.linspace(0, 1, num_points), np.arange(len(river_coords)), [c[0] for c in river_coords]) + np.random.normal(0, 0.01, num_points),
    'lon': np.interp(np.linspace(0, 1, num_points), np.arange(len(river_coords)), [c[1] for c in river_coords]) + np.random.normal(0, 0.01, num_points),
    'water_usage_m3': np.random.randint(10000, 500000, num_points), # Объем в м3 в год
    'sector': ['Agro' if i % 1 == 0 else 'Industry' for i in range(num_points)] # Все точки - АПК
}

df = pd.DataFrame(data)

# 2. Статистический расчет
total_water_usage = df['water_usage_m3'].sum()
avg_water_usage = df['water_usage_m3'].mean()
max_usage_point = df.loc[df['water_usage_m3'].idxmax()]

print(f"--- Статистика использования воды в р. Кумбель (АПК) ---")
print(f"Общий объем водозабора: {total_water_usage:,} м3/год")
print(f"Средний объем на одну точку: {avg_water_usage:,.2f} м3/год")
print(f"Максимальный забор: {max_usage_point['water_usage_m3']:,} м3/год (Точка №{max_usage_point['point_id']})")

# 3. Визуализация на карте
# Создаем карту, центрированную по реке
m = folium.Map(location=[52.22, 63.80], zoom_start=9, tiles='OpenStreetMap')

# Рисуем русло реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.7, tooltip="Река Кумбель").add_to(m)

# Функция для определения цвета маркера в зависимости от объема
def get_color(usage):
    if usage > 300000:
        return 'red'
    elif usage > 150000:
        return 'orange'
    else:
        return 'green'

# Добавляем точки водозабора
marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['water_usage_m3'] / 20000, # Размер зависит от объема
        color=get_color(row['water_usage_m3']),
        fill=True,
        fill_color=get_color(row['water_usage_m3']),
        fill_opacity=0.6,
        popup=f"Точка №{row['point_id']}<br>Сектор: АПК<br>Объем: {row['water_usage_m3']:,} м3/год"
    ).add_to(marker_cluster)

# Сохранение карты
m.save("37.html")
print("\nКарта успешно сохранена в файл 37.html")