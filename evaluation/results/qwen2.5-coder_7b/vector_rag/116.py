import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для демонстрации (если они есть в контексте)
coordinates = [
    {"name": "Tekeli River", "wkt": "POINT(35.1234 39.5678)"},
    {"name": "Lepsy River", "wkt": "POINT(35.2345 39.6789)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("116.html")