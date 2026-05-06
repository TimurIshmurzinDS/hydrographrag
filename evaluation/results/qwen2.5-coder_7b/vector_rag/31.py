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

# Если в контексте есть координаты (WKT), создаем список словарей
coordinates = [
    {"name": "Ili River", "geometry": wkt.loads("POINT(45.1234 78.9012)"), "properties": {"Water_consumption_Value": 100, "Water_level_Value": 150}}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker([coord["geometry"].y, coord["geometry"].x], popup=f"{coord['name']}<br>Consumption: {coord['properties']['Water_consumption_Value']} m³<br>Level: {coord['properties']['Water_level_Value']} m").add_to(m)

# Сохранение карты
m.save("31.html")