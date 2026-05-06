import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Polygon
import folium

# 1. Симуляция данных (так как внешние файлы отсутствуют)
# Создаем координаты для рек (условно в районе Алматинской области)
rivers_data = {
    'name': ['Tekeli River', 'Temirlik River', 'Other River'],
    'geometry': [
        LineString([(77.5, 43.2), (77.6, 43.3), (77.7, 43.25)]), # Tekeli
        LineString([(77.8, 43.1), (77.9, 43.2), (78.0, 43.15)]), # Temirlik
        LineString([(78.1, 43.0), (78.2, 43.1)])                # Other
    ]
}

# Создаем координаты для сельхозугодий (полигоны)
agri_data = {
    'field_id': [1, 2, 3, 4],
    'geometry': [
        Polygon([(77.51, 43.21), (77.55, 43.21), (77.55, 43.25), (77.51, 43.25)]), # Рядом с Tekeli
        Polygon([(77.61, 43.26), (77.65, 43.26), (77.65, 43.30), (77.61, 43.30)]), # Рядом с Tekeli
        Polygon([(77.81, 43.11), (77.85, 43.11), (77.85, 43.15), (77.81, 43.15)]), # Рядом с Temirlik
        Polygon([(78.11, 43.01), (78.15, 43.01), (78.15, 43.05), (78.11, 43.05)]), # Рядом с Other
    ]
}

# Создание GeoDataFrames
gdf_rivers = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")
gdf_agri = gpd.GeoDataFrame(agri_data, crs="EPSG:4326")

# 2. Фильтрация рек
target_rivers = gdf_rivers[gdf_rivers['name'].isin(['Tekeli River', 'Temirlik River'])]

# 3. Создание буферных зон
# Переводим в метрическую систему (EPSG:3857) для корректного расчета буфера в метрах
gdf_rivers_metric = target_rivers.to_crs(epsg=3857)
gdf_agri_metric = gdf_agri.to_crs(epsg=3857)

# Создаем буфер 5 км (5000 метров)
buffer_dist = 5000 
rivers_buffer = gdf_rivers_metric.copy()
rivers_buffer['geometry'] = rivers_buffer.geometry.buffer(buffer_dist)

# 4. Пространственное пересечение
# Находим поля, которые попадают в буфер рек
intersected_agri = gpd.overlay(gdf_agri_metric, rivers_buffer, how='intersection')

# 5. Расчет потребления воды
# Константа: норма потребления воды (например, 5000 м3 на 1 гектар)
WATER_NORM_PER_HA = 5000 

# Вычисляем площадь в квадратных метрах, затем переводим в гектары (1 га = 10 000 м2)
intersected_agri['area_ha'] = intersected_agri.geometry.area / 10000
intersected_agri['water_consumption'] = intersected_agri['area_ha'] * WATER_NORM_PER_HA

total_water = intersected_agri['water_consumption'].sum()

print(f"Общее потребление воды для сельского хозяйства: {total_water:.2f} м3")

# 6. Визуализация
# Возвращаем данные в WGS84 для folium
target_rivers_wgs = target_rivers.to_crs(epsg=4326)
intersected_agri_wgs = intersected_agri.to_crs(epsg=4326)

m = folium.Map(location=[43.2, 77.7], zoom_start=9, tiles='OpenStreetMap')

# Добавляем реки на карту
for idx, row in target_rivers_wgs.iterrows():
    coords = [(p[1], p[0]) for p in row.geometry.coords]
    folium.PolyLine(coords, color='blue', weight=4, popup=row['name']).add_to(m)

# Добавляем орошаемые поля на карту
for idx, row in intersected_agri_wgs.iterrows():
    coords = [ (p[1], p[0]) for p in row.geometry.exterior.coords ]
    folium.Polygon(coords, color='green', fill=True, fill_opacity=0.5, 
                   popup=f"Потребление: {row['water_consumption']:.1f} м3").add_to(m)

m.save("107.html")