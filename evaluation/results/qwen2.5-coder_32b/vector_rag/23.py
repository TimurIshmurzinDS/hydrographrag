import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных водного бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты точки наблюдения (пример, так как точные координаты не предоставлены)
observations = [
    {"name": "Observation Point", "geometry": wkt.loads("POINT(37.618423 55.755826)")}  # Примерные координаты Москвы
]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("23.html")