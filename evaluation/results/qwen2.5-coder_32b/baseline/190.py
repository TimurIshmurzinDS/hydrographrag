import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoJSON файлы с данными о реке и сельскохозяйственных угодиях.
river_gdf = gpd.read_file('path_to_river.geojson')
current_agriculture_gdf = gpd.read_file('path_to_current_agriculture.geojson')
planned_agriculture_gdf = gpd.read_file('path_to_planned_agriculture.geojson')

# Шаг 2: Подготовка данных
river_gdf.crs = {'init': 'epsg:4326'}
current_agriculture_gdf.crs = {'init': 'epsg:4326'}
planned_agriculture_gdf.crs = {'init': 'epsg:4326'}

# Шаг 3: Моделирование водного потока
# Для простоты предположим, что мы используем простую модель для оценки изменения водного потока.
# В реальном проекте здесь могла бы быть более сложная гидрологическая модель.

def estimate_water_flow(agriculture_gdf):
    # Простая модель: каждое сельскохозяйственное угодие влияет на водный поток
    return len(agriculture_gdf) * 100  # Предположим, что каждое угодье добавляет 100 единиц к нагрузке

current_water_flow = estimate_water_flow(current_agriculture_gdf)
planned_water_flow = estimate_water_flow(planned_agriculture_gdf)

# Шаг 4: Оценка влияния сельскохозяйственных угодий
increase_in_load = planned_water_flow - current_water_flow

# Шаг 5: Визуализация результатов
m = folium.Map(location=[river_gdf.centroid.y.mean(), river_gdf.centroid.x.mean()], zoom_start=10)

# Добавление реки на карту
folium.GeoJson(river_gdf).add_to(m)

# Добавление текущих сельскохозяйственных угодий
folium.GeoJson(current_agriculture_gdf, style_function=lambda x: {'color': 'green'}).add_to(m)

# Добавление планируемых сельскохозяйственных угодий
folium.GeoJson(planned_agriculture_gdf, style_function=lambda x: {'color': 'red'}).add_to(m)

# Добавление информации о нагрузке
folium.Marker(
    location=[river_gdf.centroid.y.mean(), river_gdf.centroid.x.mean()],
    popup=f"Текущая нагрузка: {current_water_flow} единиц\nПланируемая нагрузка: {planned_water_flow} единиц\nУвеличение нагрузки: {increase_in_load} единиц"
).add_to(m)

# Сохранение карты
m.save("190.html")