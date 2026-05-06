import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты Karatal River (пример, нужно заменить реальными данными)
karatal_river_coords = [
    {"name": "Karatal River", "wkt": "POINT(45.1234 78.9012)"}
]

# Добавление Karatal River на карту
for river in karatal_river_coords:
    point = wkt.loads(river["wkt"])
    folium.Marker([point.y, point.x], popup=f"{river['name']}<br>Water Consumption: {Water_consumption_Value} м³").add_to(m)

# Сохранение карты
m.save("214.html")