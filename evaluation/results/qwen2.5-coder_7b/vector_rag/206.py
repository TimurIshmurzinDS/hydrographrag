import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
m = folium.Map(location=[basin_data.geometry.centroid.y.mean(), basin_data.geometry.centroid.x.mean()], tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат (WKT) для демонстрации
coordinates = [
    {"name": "Kishi Osek River", "wkt": "POINT(37.5641 42.8917)"},
    {"name": "Aksu River", "wkt": "POINT(37.5641 42.8917)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты
m.save("206.html")