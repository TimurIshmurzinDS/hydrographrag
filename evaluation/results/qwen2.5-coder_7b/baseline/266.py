import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Загрузка данных о полевых участках (пример: shapefile)
fields = gpd.read_file('path_to_your_fields_shapefile.shp')

# Загрузка данных о границе бассейна реки Караой (пример: shapefile)
basin_boundary = gpd.read_file('path_to_your_basin_boundary_shapefile.shp')

# Фильтрация полевых участков, которые находятся внутри границы бассейна
fields_in_basin = fields[fields.within(basin_boundary.unary_union)]

# Генерация маршрутов полива (пример: простой маршрут - центр поля)
routes = []
for idx, row in fields_in_basin.iterrows():
    centroid = row.geometry.centroid
    routes.append([centroid.x, centroid.y])

# Создание карты с визуализацией полевых участков и маршрутов полива
m = folium.Map(location=[fields_in_basin.geometry.centroid.y.mean(), fields_in_basin.geometry.centroid.x.mean()], zoom_start=12)

# Добавление полевых участков на карту
folium.GeoJson(fields_in_basin.to_json()).add_to(m)

# Добавление маршрутов полива на карту
for route in routes:
    folium.Marker(route, icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в HTML файл
m.save("266.html")