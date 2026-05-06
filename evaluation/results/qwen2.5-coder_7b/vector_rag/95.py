import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для речей (если они доступны)
river_shyzyn_coords = [
    {"name": "Shyzhyn River", "wkt": "POINT(76.12345 43.67890)"},  # Пример WKT координат
    {"name": "Ulken Almaty River", "wkt": "POINT(76.54321 43.21098)"}  # Пример WKT координат
]

# Добавление точек на карту для речей (если доступны)
for river in river_shyzyn_coords:
    point = wkt.loads(river["wkt"])
    folium.Marker([point.y, point.x], popup=river["name"], icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("95.html")