import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs(epsg=4326)

# Инициализация карты с центром по центроиду бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты датчиков (WKT) для визуализации
sensors = [
    {"name": "Токыраун Река", "wkt": "POINT(76.93 42.85)"},
    {"name": "Аягоз Река", "wkt": "POINT(77.01 42.90)"}
]

# Добавление маркеров датчиков на карту
for sensor in sensors:
    point = wkt.loads(sensor["wkt"])
    folium.Marker([point.y, point.x], popup=sensor["name"]).add_to(m)

# Сохранение карты в файл
m.save("146.html")