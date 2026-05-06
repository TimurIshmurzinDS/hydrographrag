import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from shapely.geometry import LineString, Polygon, Point

# 1. Генерация синтетических данных для реки Лепси и агрополей
# В реальном сценарии здесь будет: river = gpd.read_file("lepsi_river.shp")
def generate_synthetic_data():
    # Координаты реки Лепси (упрощенно)
    river_coords = [
        (78.5, 44.5), (78.6, 44.6), (78.7, 44.55), 
        (78.8, 44.65), (78.9, 44.7), (79.0, 44.6)
    ]
    river_line = LineString(river_coords)
    gdf_river = gpd.GeoDataFrame({'id': [1], 'geometry': [river_line], 'crs': 'EPSG:4326'})

    # Генерация случайных сельскохозяйственных полей вокруг реки
    fields = []
    for i in range(15):
        # Создаем случайные точки вокруг реки и превращаем их в небольшие полигоны
        base_x = np.random.uniform(78.5, 79.0)
        base_y = np.random.uniform(44.5, 44.7)
        # Создаем квадратный полигон 0.01 x 0.01 градуса
        poly = Polygon([
            (base_x, base_y), (base_x + 0.01, base_y), 
            (base_x + 0.01, base_y + 0.01), (base_x, base_y + 0.01)
        ])
        fields.append(poly)
    
    gdf_fields = gpd.GeoDataFrame({'field_id': range(len(fields)), 'geometry': fields, 'crs': 'EPSG:4326'})
    return gdf_river, gdf_fields

# 2. Моделирование влияния
def analyze_agricultural_impact(gdf_river, gdf_fields):
    # Переводим в метрическую систему (UTM) для корректного расчета буферов в метрах
    # Для данного региона используем EPSG:32642 (WGS 84 / UTM zone 42N)
    river_utm = gdf_river.to_crs(epsg=32642)
    fields_utm = gdf_fields.to_crs(epsg=32642)

    # Создаем буфер влияния (например, 500 метров)
    buffer_dist = 500 
    river_buffer = river_utm.buffer(buffer_dist)
    gdf_buffer = gpd.GeoDataFrame({'geometry': river_buffer}, crs='EPSG:32642')

    # Находим пересечение полей с буфером
    intersection = gpd.overlay(gdf_buffer, fields_utm, how='intersection')
    
    # Считаем общую площадь полей внутри буфера
    total_agro_area = intersection.geometry.area.sum()
    total_buffer_area = gdf_buffer.geometry.area.sum()
    
    # Индекс влияния (от 0 до 1)
    impact_level = total_agro_area / total_buffer_area if total_buffer_area > 0 else 0
    
    return impact_level, gdf_buffer.to_crs(epsg=4326), fields_utm.to_crs(epsg=4326)

# --- Main Execution ---

# Подготовка данных
gdf_river, gdf_fields = generate_synthetic_data()
impact_score, gdf_buffer, gdf_fields_final = analyze_agricultural_impact(gdf_river, gdf_fields)

# Визуализация с помощью Folium
m = folium.Map(location=[44.6, 78.7], zoom_start=9, tiles='CartoDB positron')

# Цвет в зависимости от уровня влияния
color_map = 'green' if impact_score < 0.2 else 'orange' if impact_score < 0.5 else 'red'

# 1. Добавляем реку
folium.PolyLine(
    locations=[(p[1], p[0]) for p in gdf_river.geometry[0].coords],
    color='blue', weight=4, label='Река Лепси'
).add_to(m)

# 2. Добавляем буферную зону влияния
folium.GeoJson(
    gdf_buffer,
    style_function=lambda x: {'fillColor': color_map, 'color': 'gray', 'weight': 1, 'fillOpacity': 0.3},
    tooltip=f"Уровень влияния агрокультуры: {impact_score:.2f}"
).add_to(m)

# 3. Добавляем сельскохозяйственные поля
folium.GeoJson(
    gdf_fields_final,
    style_function=lambda x: {'fillColor': 'yellow', 'color': 'goldenrod', 'weight': 1, 'fillOpacity': 0.6},
    tooltip="Сельхозугодья"
).add_to(m)

# Добавляем легенду через HTML
legend_html = f'''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 100px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень влияния:</b><br>
     Цвет зоны: {color_map}<br>
     Индекс: {impact_score:.2f}
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("42.html")

print(f"Modeling complete. Impact Score: {impact_score:.4f}. Map saved as 42.html")