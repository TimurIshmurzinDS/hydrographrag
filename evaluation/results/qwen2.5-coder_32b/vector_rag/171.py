import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точек слияния рек в формате WKT
points_wkt = [
    {"name": "Слияние Киши-Осек", "wkt": "POINT(45.123 40.456)"},
    {"name": "Слияние Талгар", "wkt": "POINT(45.789 40.123)"}
]

# Преобразование WKT в геометрические объекты и добавление на карту
for point in points_wkt:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"]).add_to(m)

# Сохранение карты в HTML файл
m.save("171.html")