import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Шынжалы
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты некоторых точек потребления воды (WKT)
consumption_points_wkt = [
    "POINT(86.95 43.15)",
    "POINT(87.00 43.20)"
]

# Преобразование WKT в геометрические объекты
consumption_points = [wkt.loads(point) for point in consumption_points_wkt]

# Добавление точек потребления воды на карту
for point in consumption_points:
    folium.Marker([point.y, point.x], popup="Точка потребления воды").add_to(m)

# Сохранение карты в файл
m.save("36.html")