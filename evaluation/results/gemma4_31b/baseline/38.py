import folium
import numpy as np
from shapely.geometry import LineString, Point

def calculate_risk(segment_midpoint, sources):
    """
    Вычисляет уровень экологического риска для конкретной точки на основе 
    расстояния до источников загрязнения и их веса.
    """
    total_risk = 0
    for source in sources:
        # Расстояние между точкой сегмента и источником (упрощенно в градусах)
        dist = np.sqrt((segment_midpoint[0] - source['coords'][0])**2 + 
                       (segment_midpoint[1] - source['coords'][1])**2)
        # Формула затухания воздействия: вес / (расстояние + константа)
        total_risk += source['weight'] / (dist**2 + 0.001)
    return total_risk

def get_color(risk_value):
    """Определяет цвет в зависимости от значения риска."""
    if risk_value < 50:
        return 'green'
    elif risk_value < 150:
        return 'orange'
    else:
        return 'red'

# 1. Координаты русла реки Каркара (упрощенная аппроксимация для модели)
# В реальном проекте здесь загружается GeoJSON или Shapefile
river_coords = [
    [43.50, 75.10], [43.52, 75.15], [43.55, 75.20], 
    [43.58, 75.22], [43.62, 75.25], [43.65, 75.30],
    [43.68, 75.35], [43.70, 75.40]
]

# 2. Потенциальные источники загрязнения (Точки, Вес)
# Вес: 10 - низкий, 50 - средний, 100 - высокий
pollution_sources = [
    {'name': 'Промзона А', 'coords': [43.53, 75.16], 'weight': 100},
    {'name': 'Сельхозпредприятие Б', 'coords': [43.60, 75.23], 'weight': 50},
    {'name': 'Поселок В', 'coords': [43.67, 75.33], 'weight': 30},
    {'name': 'Склад Г', 'coords': [43.56, 75.21], 'weight': 70},
]

# Создание карты
m = folium.Map(location=[43.60, 75.25], zoom_start=10, tiles='CartoDB positron')

# 3. Обработка сегментов реки и расчет риска
for i in range(len(river_coords) - 1):
    p1 = river_coords[i]
    p2 = river_coords[i+1]
    
    # Находим середину сегмента для расчета риска
    midpoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    
    risk_val = calculate_risk(midpoint, pollution_sources)
    color = get_color(risk_val)
    
    # Рисуем сегмент реки
    folium.PolyLine(
        locations=[p1, p2],
        color=color,
        weight=5,
        opacity=0.8,
        tooltip=f"Уровень риска: {round(risk_val, 2)}"
    ).add_to(m)

# 4. Добавление источников загрязнения на карту
for source in pollution_sources:
    folium.CircleMarker(
        location=source['coords'],
        radius=6,
        color='black',
        fill=True,
        fill_color='gray',
        popup=f"{source['name']} (Вес: {source['weight']})"
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень риска:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("38.html")
print("Модель успешно построена. Результат сохранен в файл 38.html")