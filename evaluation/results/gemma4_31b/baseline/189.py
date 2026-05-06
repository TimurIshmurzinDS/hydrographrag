import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd
import random

# 1. Определение области интереса (Регион реки Турген, Казахстан/Центральная Азия)
# Приблизительные координаты бассейна реки Турген
CENTER_LAT = 43.15
CENTER_LON = 79.10
RADIUS = 0.2  # Радиус охвата в градусах

def generate_synthetic_data():
    """Генерация синтетических данных для моделирования засухи и ирригации"""
    # Создаем сетку точек для расчета вероятности засухи
    grid_points = []
    for lat in np.linspace(CENTER_LAT - RADIUS, CENTER_LAT + RADIUS, 20):
        for lon in np.linspace(CENTER_LON - RADIUS, CENTER_LON + RADIUS, 20):
            # Вероятность засухи зависит от удаленности от реки (условно) и случайного фактора
            # Имитируем градиент: чем выше в горы или дальше от русла, тем выше риск
            prob = random.uniform(0.1, 0.9) 
            grid_points.append([lat, lon, prob])
    
    # Создаем точки ирригационных систем (каналы, насосные станции)
    irrigation_systems = []
    for i in range(15):
        lat = random.uniform(CENTER_LAT - RADIUS, CENTER_LAT + RADIUS)
        lon = random.uniform(CENTER_LON - RADIUS, CENTER_LON + RADIUS)
        # Определяем риск для конкретного объекта на основе его положения
        # В реальности здесь был бы пространственный запрос к слою засухи
        risk_level = random.choice(['Low', 'Medium', 'High'])
        irrigation_systems.append({'id': i, 'lat': lat, 'lon': lon, 'risk': risk_level})
        
    return grid_points, irrigation_systems

# 2. Основной процесс моделирования
grid_data, irrigation_data = generate_synthetic_data()

# Создание карты Folium
m = folium.Map(location=[CENTER_LAT, CENTER_LON], zoom_start=11, tiles='OpenStreetMap')

# 3. Визуализация вероятности засухи (HeatMap)
# HeatMap принимает список [lat, lon, weight]
heat_data = [[p[0], p[1], p[2]] for p in grid_data]
HeatMap(heat_data, name="Вероятность засухи", radius=25, blur=15, min_opacity=0.5).add_to(m)

# 4. Визуализация ирригационных систем и их уязвимости
color_map = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}

for sys in irrigation_data:
    folium.CircleMarker(
        location=[sys['lat'], sys['lon']],
        radius=7,
        popup=f"Ирригационный узел {sys['id']}<br>Риск засухи: {sys['risk']}",
        color=color_map[sys['risk']],
        fill=True,
        fill_color=color_map[sys['risk']],
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 110px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда рисков:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий риск<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний риск<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий риск<br>
     <br>
     <span style="color:blue">Тепловая карта: Вероятность засухи</span>
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("189.html")

print("Моделирование завершено. Карта сохранена в файл 189.html")