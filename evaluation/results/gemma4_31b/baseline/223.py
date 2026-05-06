import folium
import pandas as pd
import numpy as np
import random

def calculate_investment_signal(water_level):
    """
    Логика определения инвестиционного сигнала на основе уровня воды.
    Диапазон: 0 - 10 метров.
    """
    if 3.0 <= water_level <= 5.0:
        return "STRONG BUY (Оптимальный уровень для добычи)", "green"
    elif 2.0 <= water_level < 3.0 or 5.0 < water_level <= 7.0:
        return "HOLD (Стабильный уровень)", "orange"
    else:
        return "AVOID (Риск засухи или наводнения)", "red"

# 1. Координаты реки Баянкол (условные координаты для демонстрации в регионе Казахстана)
# В реальном проекте здесь будет загрузка GeoJSON или Shapefile
river_coords = [
    [45.123, 68.456], [45.150, 68.500], [45.180, 68.550], 
    [45.210, 68.600], [45.250, 68.650], [45.300, 68.700]
]

# 2. Симуляция данных по датчикам уровня воды
sensors_data = {
    'sensor_id': [1, 2, 3],
    'lat': [45.150, 45.210, 45.300],
    'lon': [68.500, 68.600, 68.700],
    'current_level': [4.2, 2.1, 8.5]  # м
}
df_sensors = pd.DataFrame(sensors_data)

# 3. Создание карты
m = folium.Map(location=[45.21, 68.57], zoom_start=10, tiles='Stamen Terrain')

# Отрисовка русла реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Bayankol River").add_to(m)

# 4. Анализ и добавление объектов на карту
for index, row in df_sensors.iterrows():
    signal, color = calculate_investment_signal(row['current_level'])
    
    # Добавляем маркер датчика
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"Датчик {row['sensor_id']}<br>Уровень: {row['current_level']}м<br>Сигнал: {signal}"
    ).add_to(m)
    
    # Создаем буферную зону вокруг датчика (зона потенциальной добычи)
    folium.Circle(
        location=[row['lat'], row['lon']],
        radius=2000, # 2 км
        color=color,
        fill=True,
        fill_opacity=0.2,
        tooltip=f"Зона влияния датчика {row['sensor_id']}"
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Инвестиционный сигнал:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> STRONG BUY (3-5м)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> HOLD (2-3м или 5-7м)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> AVOID (<2м или >7м)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("223.html")

print("Modeling complete. The map has been saved as 223.html")