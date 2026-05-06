import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водных бассейнах
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в среднем значении координат водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты точек рек (примерные данные)
coordinates = [
    {"name": "Byzhy River", "wkt": "POINT(76.95 48.35)"},
    {"name": "Urzhar River", "wkt": "POINT(77.05 48.25)"}
]

# Добавление точек рек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("204.html")