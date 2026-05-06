import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных наблюдений (замените на реальные данные)
observations = [
    {'date': '2023-04-01', 'flow_rate': 50},
    {'date': '2023-04-02', 'flow_rate': 60},
    {'date': '2023-04-03', 'flow_rate': 55},
    {'date': '2023-04-04', 'flow_rate': 58}
]

# Визуализация данных наблюдений (пример)
for obs in observations:
    folium.Marker([centroid.y, centroid.x], popup=f"Flow Rate: {obs['flow_rate']} m³/s").add_to(m)

# Сохранение карты
m.save("17.html")