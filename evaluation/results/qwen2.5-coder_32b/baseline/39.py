import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame с данными о бассейне реки Или и зонах полива.
# Для примера создадим эти данные искусственно.

# Создание полигона для бассейна реки Или (координаты примерные)
ili_basin_coords = [
    (45.9, 10.2), (46.1, 10.3), (46.2, 10.1), 
    (46.0, 9.9), (45.8, 10.0)
]
ili_basin = Polygon(ili_basin_coords)

# Создание точек для зон полива
irrigation_points_coords = [
    (45.95, 10.25), (46.05, 10.2), (46.1, 10.15)
]
irrigation_points = [Point(coord) for coord in irrigation_points_coords]

# Создание GeoDataFrame для бассейна реки Или
ili_basin_gdf = gpd.GeoDataFrame({'name': ['Бассейн реки Или'], 'geometry': [ili_basin]})

# Создание GeoDataFrame для зон полива с объемами воды (примерные данные)
irrigation_gdf = gpd.GeoDataFrame({
    'point_id': range(1, 4),
    'water_volume_m3': [5000, 7000, 6000],
    'geometry': irrigation_points
})

# Шаг 2: Обработка данных (в данном случае данные уже подготовлены)

# Шаг 3: Моделирование (просто суммируем объемы воды для примера)
total_water_volume = irrigation_gdf['water_volume_m3'].sum()

print(f"Общий объем воды, используемой для полива в бассейне реки Или: {total_water_volume} м³")

# Шаг 4: Визуализация
# Создание карты с использованием folium
m = folium.Map(location=[46.0, 10.2], zoom_start=10)

# Добавление бассейна реки Или на карту
folium.GeoJson(ili_basin_gdf).add_to(m)

# Добавление точек полива с метками объемов воды
for _, row in irrigation_gdf.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f"Объем воды: {row['water_volume_m3']} м³",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Сохранение карты в файл
m.save("39.html")