import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Баянколь
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат наблюдательных пунктов (WKT)
observations_wkt = [
    "POINT(87.6543 49.1234)",
    "POINT(87.6553 49.1244)",
    "POINT(87.6563 49.1254)",
    "POINT(87.6573 49.1264)"
]

# Преобразование WKT в точки и добавление на карту
observations = [wkt.loads(obs) for obs in observations_wkt]
for point in observations:
    folium.Marker([point.y, point.x], popup="Observation Point").add_to(m)

# Сохранение карты
m.save("215.html")