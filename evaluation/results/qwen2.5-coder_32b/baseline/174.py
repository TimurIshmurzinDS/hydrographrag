import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Загрузка данных о водоразделах
# Предположим, что у нас есть файл GeoJSON с водоразделами
watershed_file = 'path_to_watersheds.geojson'
gdf_watersheds = gpd.read_file(watershed_file)

# Шаг 2: Фильтрация данных для рек Эмель и Тентек
# Предположим, что в атрибутах есть поле 'river_name' с названиями рек
gdf_emel = gdf_watersheds[gdf_watersheds['river_name'] == 'Эмель']
gdf_tentek = gdf_watersheds[gdf_watersheds['river_name'] == 'Тентек']

# Шаг 3: Определение пересечений водоразделов
intersection_points = []
for geom_emel in gdf_emel.geometry:
    for geom_tentek in gdf_tentek.geometry:
        intersection = geom_emel.intersection(geom_tentek)
        if not intersection.is_empty and isinstance(intersection, Point):
            intersection_points.append(intersection)

# Преобразование точек пересечений в GeoDataFrame
gdf_intersections = gpd.GeoDataFrame(geometry=intersection_points, crs=gdf_watersheds.crs)

# Шаг 4: Визуализация на карте с помощью folium
# Выбор центральной точки для карты (например, среднее значение координат)
center_lat = gdf_intersections.geometry.y.mean()
center_lon = gdf_intersections.geometry.x.mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Добавление водоразделов рек Эмель и Тентек на карту
folium.GeoJson(gdf_emel).add_to(m)
folium.GeoJson(gdf_tentek).add_to(m)

# Добавление точек пересечений на карту
for _, row in gdf_intersections.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup='Точка пересечения',
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("174.html")