import folium
import numpy as np
from folium.plugins import HeatMap

def calculate_pollution(point, sources):
    """
    Вычисляет уровень загрязнения в точке на основе расстояния до источников.
    """
    total_pollution = 0
    for source in sources:
        # Евклидово расстояние (упрощенно для малых масштабов)
        dist = np.sqrt((point[0] - source['coords'][0])**2 + (point[1] - source['coords'][1])**2)
        # Модель затухания: интенсивность / (расстояние + константа)
        total_pollution += source['intensity'] / (dist + 0.01)**2
    return total_pollution

# 1. Координаты русла реки Талгар (упрощенная аппроксимация)
# В реальном проекте здесь будет загрузка GeoJSON или Shapefile
river_coords = [
    [43.15, 77.30], [43.12, 77.35], [43.10, 77.40], 
    [43.08, 77.45], [43.05, 77.50], [43.02, 77.55], 
    [43.00, 77.60], [42.98, 77.65], [42.95, 77.70]
]

# 2. Потенциальные источники загрязнения (заводы, стоки)
pollution_sources = [
    {"name": "Industrial Zone A", "coords": [43.11, 77.38], "intensity": 0.005},
    {"name": "Urban Settlement B", "coords": [43.06, 77.48], "intensity": 0.008},
    {"name": "Waste Plant C", "coords": [42.97, 77.68], "intensity": 0.012},
]

# 3. Расчет уровней загрязнения вдоль реки
pollution_levels = []
for pt in river_coords:
    level = calculate_pollution(pt, pollution_sources)
    pollution_levels.append(level)

# Нормализация уровней для визуализации (от 0 до 1)
max_p = max(pollution_levels)
min_p = min(pollution_levels)
norm_levels = [(p - min_p) / (max_p - min_p) for p in pollution_levels]

# 4. Визуализация с помощью folium
m = folium.Map(location=[43.05, 77.50], zoom_start=10, tiles='CartoDB positron')

# Отрисовка сегментов реки с разным цветом в зависимости от загрязнения
for i in range(len(river_coords) - 1):
    start = river_coords[i]
    end = river_coords[i+1]
    
    # Определяем цвет: Зеленый (чисто) -> Желтый -> Красный (грязно)
    val = norm_levels[i]
    color = 'green' if val < 0.3 else 'orange' if val < 0.7 else 'red'
    
    folium.PolyLine(
        locations=[start, end],
        color=color,
        weight=5,
        opacity=0.8,
        tooltip=f"Уровень загрязнения: {round(pollution_levels[i], 4)}"
    ).add_to(m)

# Добавление маркеров источников
for source in pollution_sources:
    folium.CircleMarker(
        location=source['coords'],
        radius=7,
        color='black',
        fill=True,
        fill_color='grey',
        popup=f"Источник: {source['name']}"
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень загрязнения:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("40.html")
print("Модель построена. Результат сохранен в файл 40.html")