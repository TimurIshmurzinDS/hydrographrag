import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# 1. Симуляция данных (так как реальные данные по р. Бутак требуют доступа к закрытым гидропостам)
# Координаты примерного расположения реки Бутак (Центральная Азия/Казахстан)
RIVER_START = [44.5, 71.0] 
RIVER_END = [44.2, 71.5]

def generate_river_points(start, end, num_points=50):
    """Генерация точек русла реки"""
    lats = np.linspace(start[0], end[0], num_points)
    lons = np.linspace(start[1], end[1], num_points)
    # Добавляем немного случайности для имитации изгибов реки
    lats += np.random.normal(0, 0.01, num_points)
    lons += np.random.normal(0, 0.01, num_points)
    return list(zip(lats, lons))

def calculate_stability(dist_to_river, seasonal_flow_variance):
    """
    Модель расчета устойчивости агроценоза.
    Устойчивость падает, если расстояние до реки велико, а колебания стока высоки.
    """
    # Базовая устойчивость 1.0, снижается при удалении и высокой вариативности стока
    stability = 1.0 - (dist_to_river * 0.5) - (seasonal_flow_variance * 0.3)
    return max(0.1, min(1.0, stability))

# 2. Параметры модели
seasonal_flow_variance = 0.4  # Коэффициент сезонных колебаний (0-1)
river_coords = generate_river_points(RIVER_START, RIVER_END)

# 3. Создание сетки агроценозов вокруг реки
agro_zones = []
for lat, lon in river_coords:
    for dx in np.arange(-0.1, 0.1, 0.02):
        for dy in np.arange(-0.1, 0.1, 0.02):
            # Расстояние до ближайшей точки реки (упрощенно)
            dist = np.sqrt(dx**2 + dy**2)
            stability = calculate_stability(dist, seasonal_flow_variance)
            agro_zones.append([lat + dx, lon + dy, stability])

# 4. Визуализация с помощью Folium
m = folium.Map(location=[44.35, 71.25], zoom_start=10, tiles='OpenStreetMap')

# Отрисовка русла реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Бутак").add_to(m)

# Отрисовка агроценозов (цветовая индикация устойчивости)
for point in agro_zones:
    lat, lon, stability = point
    # Цвет: Красный (низкая устойчивость) -> Зеленый (высокая)
    color = 'red' if stability < 0.4 else 'orange' if stability < 0.7 else 'green'
    
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"Stability Index: {stability:.2f}"
    ).add_to(m)

# Добавление легенды (текстовый объект)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Устойчивость агроценозов</b><br>
     <i style="background:green;width:10px;height:10px;display:inline-block"></i> Высокая<br>
     <i style="background:orange;width:10px;height:10px;display:inline-block"></i> Средняя<br>
     <i style="background:red;width:10px;height:10px;display:inline-block"></i> Низкая
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("192.html")

print("Modeling complete. The map has been saved as 192.html")