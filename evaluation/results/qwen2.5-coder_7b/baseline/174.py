import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о водоразделах для рек Эмель и Тентек
emel_crossings = gpd.read_file('path_to_emel_crossings.shp')
tentek_crossings = gpd.read_file('path_to_tentek_crossings.shp')

# Фильтрация данных, чтобы получить только водоразделы между реками Эмель и Тентек
emel_crossings_filtered = emel_crossings[emel_crossings.within(tentek_crossings.unary_union)]
tentek_crossings_filtered = tentek_crossings[tentek_crossings.within(emel_crossings.unary_union)]

# Определение пересечений водоразделов
intersection_points = []
for line1 in emel_crossings_filtered.geometry:
    for line2 in tentek_crossings_filtered.geometry:
        intersection = line1.intersection(line2)
        if not intersection.is_empty:
            intersection_points.append(intersection)

# Создание GeoDataFrame для точек пересечения
intersection_gdf = gpd.GeoDataFrame(geometry=intersection_points, crs=emel_crossings.crs)

# Визуализация результатов на карте
m = folium.Map(location=[intersection_gdf.geometry.centroid.y.mean(), intersection_gdf.geometry.centroid.x.mean()], zoom_start=10)

for point in intersection_gdf.geometry:
    folium.Marker([point.y, point.x], popup='Пересечение').add_to(m)

# Сохранение карты
m.save("174.html")