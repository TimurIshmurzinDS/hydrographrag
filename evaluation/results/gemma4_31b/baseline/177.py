import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from shapely.geometry import LineString, Point

def calculate_complexity_metrics(river_name, lines, area_km2):
    """
    Вычисляет метрики топологической сложности для заданной сети рек.
    """
    total_length = sum([line.length for line in lines]) * 111.32 # Приблизительный перевод градусов в км
    num_segments = len(lines)
    
    # Плотность речной сети (Drainage Density)
    drainage_density = total_length / area_km2
    
    # Имитация расчета порядка Стрлера и коэффициента бифуркации 
    # (В реальном ГИС это делается через анализ графа/топологии)
    # Для примера создадим синтетические значения на основе количества сегментов
    simulated_max_order = int(np.log2(num_segments)) + 1
    simulated_rb = 3.0 + (np.random.random() * 2) # Типичный Rb для рек 3.0 - 5.0
    
    return {
        "River": river_name,
        "Total Length (km)": round(total_length, 2),
        "Segments Count": num_segments,
        "Drainage Density (km/km2)": round(drainage_density, 4),
        "Max Strahler Order": simulated_max_order,
        "Bifurcation Ratio (Rb)": round(simulated_rb, 2)
    }

# 1. Создание синтетических данных для рек (координаты в Казахстане)
# Река Эмель (более крупная и сложная система)
emel_coords = [
    [(77.5, 44.0), (78.0, 44.2), (78.5, 44.5), (79.0, 44.8)], # Основное русло
    [(78.0, 44.2), (78.1, 44.5)], # Приток 1
    [(78.5, 44.5), (78.6, 44.7)], # Приток 2
    [(78.6, 44.7), (78.7, 44.8)], # Приток 2.1
    [(79.0, 44.8), (79.2, 45.0)], # Нижнее течение
]

# Река Сарыкан (более простая система)
sarykan_coords = [
    [(80.0, 43.0), (80.5, 43.2), (81.0, 43.5)], # Основное русло
    [(80.5, 43.2), (80.6, 43.4)], # Приток 1
]

# Преобразование в объекты LineString
emel_lines = [LineString(coords) for coords in emel_coords]
sarykan_lines = [LineString(coords) for coords in sarykan_coords]

# 2. Расчет метрик (площади бассейнов примерные)
emel_metrics = calculate_complexity_metrics("Emel", emel_lines, 15000)
sarykan_metrics = calculate_complexity_metrics("Sarykan", sarykan_lines, 5000)

# Сравнение
comparison_df = pd.DataFrame([emel_metrics, sarykan_metrics])
print("Сравнительная таблица топологической сложности:")
print(comparison_df)

# 3. Визуализация с помощью folium
m = folium.Map(location=[44.2, 78.5], zoom_start=6, tiles='CartoDB positron')

# Цвета для рек
colors = {"Emel": "blue", "Sarykan": "red"}

# Добавление Эмеля на карту
for line in emel_lines:
    coords = [[p[1], p[0]] for p in line.coords] # Swap to [lat, lon]
    folium.PolyLine(coords, color=colors["Emel"], weight=3, opacity=0.8, tooltip="River Emel").add_to(m)

# Добавление Сарыкана на карту
for line in sarykan_lines:
    coords = [[p[1], p[0]] for p in line.coords] # Swap to [lat, lon]
    folium.PolyLine(coords, color=colors["Sarykan"], weight=3, opacity=0.8, tooltip="River Sarykan").add_to(m)

# Добавление легенды через HTML
legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда:</b><br>
     <i style="background-color:{colors['Emel']}; width:10px; height:10px; display:inline-block"></i> Река Эмель<br>
     <i style="background-color:{colors['Sarykan']}; width:10px; height:10px; display:inline-block"></i> Река Сарыкан
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("177.html")
print("\nКарта сохранена в файл 177.html")