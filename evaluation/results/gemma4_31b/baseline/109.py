import folium
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd

# 1. Создание синтетических данных для рек (координаты для демонстрации)
# В реальном сценарии здесь будет загрузка из .shp или .geojson файлов
data = {
    'river_name': ['Byzhy River', 'Lepsy River'],
    'geometry': [
        # Имитация русла реки Byzhy
        LineString([(70.1, 45.1), (70.2, 45.2), (70.3, 45.15), (70.4, 45.3)]),
        # Имитация русла реки Lepsy
        LineString([(70.5, 45.1), (70.6, 45.1), (70.7, 45.2), (70.8, 45.4), (70.9, 45.5)])
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# 2. Перевод в проекционную систему координат для точных расчетов в метрах (EPSG:3857)
gdf_projected = gdf.to_crs(epsg=3857)

# 3. Расчет длины рек
gdf_projected['length_m'] = gdf_projected.geometry.length

# 4. Анализ доступности: создание буфера 500 метров
buffer_dist = 500 
gdf_projected['buffer_zone'] = gdf_projected.geometry.buffer(buffer_dist)
gdf_projected['access_area_sqm'] = gdf_projected['buffer_zone'].area

# Возвращаем данные в WGS84 для визуализации
gdf_final = gdf_projected.to_crs(epsg=4326)
# Переносим буферы в WGS84
gdf_final['buffer_zone'] = gdf_projected['buffer_zone'].to_crs(epsg=4326)

# Вывод результатов сравнения в консоль
print("Сравнительный анализ доступности водных ресурсов:")
print(gdf_projected[['river_name', 'length_m', 'access_area_sqm']])

# 5. Визуализация на карте
# Центрируем карту по средним координатам
center_lat = gdf.geometry.centroid.y.mean()
center_lon = gdf.geometry.centroid.x.mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles='CartoDB positron')

colors = {'Byzhy River': 'blue', 'Lepsy River': 'green'}

for idx, row in gdf_final.iterrows():
    name = row['river_name']
    color = colors[name]
    
    # Добавление линии реки
    folium.PolyLine(
        locations=[(p[1], p[0]) for p in row['geometry'].coords],
        color=color,
        weight=4,
        tooltip=f"River: {name}"
    ).add_to(m)
    
    # Добавление буферной зоны (доступности)
    # Преобразуем геометрию буфера в список координат для folium
    if row['buffer_zone'].geom_type == 'Polygon':
        coords = [(p[1], p[0]) for p in row['buffer_zone'].exterior.coords]
        folium.Polygon(
            locations=coords,
            color=color,
            fill=True,
            fill_opacity=0.2,
            weight=1,
            tooltip=f"Access Zone: {name}"
        ).add_to(m)

# Сохранение карты
m.save("109.html")
print("\nКарта доступности ресурсов сохранена в файл 109.html")