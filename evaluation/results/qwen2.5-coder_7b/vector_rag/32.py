import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат WKT для добавления маркеров (если есть)
coordinates_wkt = [
    {"name": "Маркер 1", "wkt": "POINT(43.6578 49.8567)"},
    {"name": "Маркер 2", "wkt": "POINT(43.6580 49.8568)"}
]

# Преобразование WKT в координаты и добавление маркеров на карту
for coord in coordinates_wkt:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты
m.save("32.html")