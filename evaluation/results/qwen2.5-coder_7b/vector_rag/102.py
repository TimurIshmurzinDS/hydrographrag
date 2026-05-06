import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для демонстрации, фактически не используется)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для точек впадения (только для демонстрации, фактически не используется)
points = [
    {"name": "Впадение Каратал", "wkt": "POINT(76.1234 45.6789)"},
    {"name": "Улькен Алматы", "wkt": "POINT(77.0123 46.5432)"}
]

# Преобразование WKT в координаты
point_coords = [(wkt.loads(point["wkt"]).x, wkt.loads(point["wkt"]).y) for point in points]

# Добавление точек на карту
for coord in point_coords:
    folium.Marker(coord, popup="Точка").add_to(m)

# Сохранение карты
m.save("102.html")