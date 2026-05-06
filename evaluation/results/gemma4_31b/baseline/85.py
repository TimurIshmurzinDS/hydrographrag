import pandas as pd
import numpy as np
import folium
from shapely.geometry import LineString, Point

# 1. Имитация данных по расходу воды (m3/s) для рек Коктал и Баскан
# В реальном сценарии здесь будет загрузка из CSV или API гидрологической службы
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Koktal_flow': [1.2, 1.5, 4.8, 6.2, 3.1, 1.1, 0.5, 0.4, 0.8, 2.1, 1.8, 1.3],
    'Baskan_flow': [0.8, 1.0, 3.5, 5.1, 2.8, 0.9, 0.3, 0.2, 0.6, 1.5, 1.2, 0.9]
}
df = pd.DataFrame(data)

# Координаты рек (упрощенные аппроксимации для демонстрации)
# Коктал (горная часть и предгорья)
koktal_coords = [
    [44.75, 18.80], [44.72, 18.85], [44.68, 18.90], [44.65, 18.95]
]
# Баскан (степная часть)
baskan_coords = [
    [44.80, 19.20], [44.75, 19.40], [44.70, 19.60], [44.60, 19.80]
]

# 2. Анализ рисков (поиск максимального сезонного расхода)
max_koktal_idx = df['Koktal_flow'].idxmax()
max_baskan_idx = df['Baskan_flow'].idxmax()

max_koktal_val = df.loc[max_koktal_idx, 'Koktal_flow']
max_baskan_val = df.loc[max_baskan_idx, 'Baskan_flow']

avg_koktal = df['Koktal_flow'].mean()
avg_baskan = df['Baskan_flow'].mean()

# 3. Функция для расчета ширины буфера (в метрах, переведенных в градусы для упрощения)
# В реальном GIS используется проекция UTM, здесь используем аппроксимацию: 1 град ~ 111км
def calculate_buffer_width(current_flow, avg_flow):
    base_width = 0.002 # Базовая ширина зоны (около 200м)
    return base_width * (current_flow / avg_flow)

koktal_buffer = calculate_buffer_width(max_koktal_val, avg_koktal)
baskan_buffer = calculate_buffer_width(max_baskan_val, avg_baskan)

# 4. Визуализация на карте
# Центр карты в районе Крыма
m = folium.Map(location=[44.7, 19.3], zoom_start=9, tiles='CartoDB positron')

def add_river_risk(m, coords, buffer_width, name, color):
    # Рисуем линию реки
    folium.PolyLine(coords, color=color, weight=3, opacity=0.8, tooltip=f"River {name}").add_to(m)
    
    # Создаем зону затопления (упрощенно через серию кругов/полигонов вдоль линии)
    for point in coords:
        folium.Circle(
            location=point,
            radius=buffer_width * 100000, # Перевод условного коэффициента в метры для folium
            color=color,
            fill=True,
            fill_opacity=0.3,
            popup=f"Risk Zone: {name} (Seasonal Peak)"
        ).add_to(m)

# Добавляем реки на карту
add_river_risk(m, koktal_coords, koktal_buffer, "Koktal", "blue")
add_river_risk(m, baskan_coords, baskan_buffer, "Baskan", "green")

# Добавляем маркеры пиковых зон
folium.Marker(
    location=koktal_coords[0], 
    popup=f"Koktal Peak: {max_koktal_val} m3/s in {df.loc[max_koktal_idx, 'Month']}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    location=baskan_coords[0], 
    popup=f"Baskan Peak: {max_baskan_val} m3/s in {df.loc[max_baskan_idx, 'Month']}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("85.html")

print("Modeling complete. The risk map has been saved as 85.html")