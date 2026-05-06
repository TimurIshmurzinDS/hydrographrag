import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдений (WKT) для демонстрации
observations = [
    {"name": "Temirlik River", "wkt": "POINT(76.9345 42.8105)"},
    {"name": "Turgen River", "wkt": "POINT(77.0345 42.9105)"},
    {"name": "Karaoy River", "wkt": "POINT(76.8345 42.7105)"}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker([point.y, point.x], popup=obs["name"]).add_to(m)

# Сохранение карты в файл
m.save("86.html")