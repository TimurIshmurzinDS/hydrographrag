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

# Предположим, что у нас есть координаты наблюдений уровней воды в реках Сарыкан и Аксу
# Эти данные представлены в формате WKT (Well-Known Text)
observations = [
    {'name': 'Sarykan River', 'wkt': 'POINT(80.25 41.3)', 'water_level': 120},  # Примерные координаты и уровень воды
    {'name': 'Aksu River', 'wkt': 'POINT(79.5 41.6)', 'water_level': 150}     # Примерные координаты и уровень воды
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.Marker([point.y, point.x], popup=f"{obs['name']}: Уровень воды {obs['water_level']} см").add_to(m)

# Сохранение карты в файл
m.save("106.html")