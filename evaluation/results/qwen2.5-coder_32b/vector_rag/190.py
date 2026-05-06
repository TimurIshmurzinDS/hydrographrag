import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдений (пример, так как точные координаты не предоставлены)
observations = [
    {"type": "Point", "coordinates": [37.5, 48.5]},  # Примерные координаты
    {"type": "Point", "coordinates": [37.6, 48.6]},
    {"type": "Point", "coordinates": [37.7, 48.7]},
    {"type": "Point", "coordinates": [37.8, 48.8]}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(f"POINT ({obs['coordinates'][0]} {obs['coordinates'][1]})")
    folium.Marker([point.y, point.x], popup="Наблюдение").add_to(m)

# Сохранение карты в файл
m.save("190.html")