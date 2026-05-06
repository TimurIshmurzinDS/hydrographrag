import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек (если есть)
coordinates = [
    {"name": "Kishi Almaty River", "wkt": "POINT(76.9345 42.8617)"},
    {"name": "Ulken Almaty River", "wkt": "POINT(76.9000 42.8500)"},
    {"name": "Kishi Osek River", "wkt": "POINT(76.9500 42.8700)"},
    {"name": "Sharyn River", "wkt": "POINT(77.1000 43.0000)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("131.html")