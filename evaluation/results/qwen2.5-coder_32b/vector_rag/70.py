import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты гидрологических постов на реке Sharyn River (WKT)
observation_points = [
    {"name": "Пост 1", "wkt": "POINT(85.3456 49.2345)"},
    {"name": "Пост 2", "wkt": "POINT(85.4567 49.3456)"},
    {"name": "Пост 3", "wkt": "POINT(85.5678 49.4567)"}
]

# Добавление маркеров на карту
for point in observation_points:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"]).add_to(m)

# Сохранение карты в файл
m.save("70.html")