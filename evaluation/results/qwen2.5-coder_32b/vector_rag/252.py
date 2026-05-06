import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Дос
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат реки Дос (WKT)
river_dos_coordinates = [
    {"name": "Point1", "wkt": "POINT(37.5 56.8)"},
    {"name": "Point2", "wkt": "POINT(37.6 56.9)"}
]

# Добавление точек реки Дос на карту
for point in river_dos_coordinates:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"]).add_to(m)

# Сохранение карты в файл
m.save("252.html")