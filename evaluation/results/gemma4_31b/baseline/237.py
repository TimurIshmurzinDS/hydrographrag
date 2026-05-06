import folium
from folium.plugins import HeatMap
import numpy as np
import random

def generate_aksu_river_coords():
    """
    Генерация имитационных координат для реки Аксу (Центральная Азия).
    В реальном проекте здесь будет загрузка GeoJSON или Shapefile.
    """
    # Примерный путь реки (упрощенно)
    start_lat, start_lon = 43.5, 81.0
    coords = []
    for i in range(20):
        lat = start_lat - (i * 0.15) + random.uniform(-0.05, 0.05)
        lon = start_lon + (i * 0.2) + random.uniform(-0.05, 0.05)
        coords.append([lat, lon])
    return coords

def create_flood_zone(river_coords, width_factor=0.02):
    """
    Создание имитации зоны затопления (полигона вокруг реки).
    """
    flood_polygons = []
    for i in range(len(river_coords) - 1):
        p1 = river_coords[i]
        p2 = river_coords[i+1]
        
        # Создаем упрощенный прямоугольник вокруг сегмента реки
        # чтобы имитировать разлив воды в пойме
        poly = [
            [p1[0] + width_factor, p1[1] + width_factor],
            [p2[0] + width_factor, p2[1] + width_factor],
            [p2[0] - width_factor, p2[1] - width_factor],
            [p1[0] - width_factor, p1[1] - width_factor]
        ]
        flood_polygons.append(poly)
    return flood_polygons

# 1. Инициализация карты
# Центрируем карту на примерном районе реки Аксу
m = folium.Map(location=[42.5, 82.0], zoom_start=7, tiles='CartoDB positron')

# 2. Подготовка данных ("Ингредиентов")
river_path = generate_aksu_river_coords()
flood_zones = create_flood_zone(river_path)

# 3. Добавление "Основы" — русла реки
folium.PolyLine(
    river_path, 
    color='blue', 
    weight=4, 
    opacity=0.8, 
    tooltip='Русло реки Аксу'
).add_to(m)

# 4. Добавление "Зоны затопления" (Поймы)
for zone in flood_zones:
    folium.Polygon(
        locations=zone,
        color='cyan',
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        weight=1,
        tooltip='Зона весеннего паводка'
    ).add_to(m)

# 5. Добавление "Снеготаяния" (Heatmap)
# Генерируем случайные точки в верховьях реки с разной интенсивностью
snowmelt_data = []
for point in river_path[:5]: # Верховья
    for _ in range(10):
        snowmelt_data.append([
            point[0] + random.uniform(-0.2, 0.2), 
            point[1] + random.uniform(-0.2, 0.2), 
            random.uniform(0.5, 1.0)
        ])

HeatMap(snowmelt_data, name="Интенсивность снеготаяния").add_to(m)

# 6. Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Рецепт 'Весенний паводок'</b><br>
     <i style="background-color:blue; width:10px; height:10px; display:inline-block"></i> Русло реки<br>
     <i style="background-color:cyan; width:10px; height:10px; display:inline-block"></i> Зона затопления<br>
     <i style="background-color:red; width:10px; height:10px; display:inline-block"></i> Снеготаяние (Heatmap)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("237.html")

print("Modeling complete. The 'Spring Flood' cocktail map has been saved as 237.html")