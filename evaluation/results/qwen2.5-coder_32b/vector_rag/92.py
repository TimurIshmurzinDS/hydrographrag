import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование его в CRS EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты folium с центром по центроиду бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты устья реки Дос и начала реки Емель
coordinates = [
    {"name": "Устье реки Дос", "wkt": "POINT(37.618423 55.755826)"},
    {"name": "Начало реки Емель", "wkt": "POINT(37.606094 55.748868)"}
]

# Добавление точек на карту и вычисление расстояния между ними
points = []
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    points.append(point)
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Вычисление расстояния между точками (в метрах) с использованием метода geopandas
distance = points[0].distance(points[1])
print(f"Расстояние между устью реки Дос и началом реки Емель: {distance:.2f} м")

# Сохранение карты в файл
m.save("92.html")