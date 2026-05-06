import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
coordinates = [
    {"type": "Point", "coordinates": [76.183, 40.592]},  # Примерные координаты реки Аксу
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(f"POINT ({coord['coordinates'][0]} {coord['coordinates'][1]})")
    folium.Marker([point.y, point.x], popup="Aksu River").add_to(m)

# Сохранение карты в файл
m.save("248.html")