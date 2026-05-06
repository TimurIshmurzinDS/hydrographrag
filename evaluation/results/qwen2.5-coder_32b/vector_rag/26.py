import geopandas as gpd
import folium
from shapely import wkt

# Загрузка геопространственных данных бассейна реки Осек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Осек
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдательных пунктов (примерные, так как точные координаты не предоставлены)
observations = [
    {"coordinates": "POINT(37.5 56.1)", "level": 150},  # Примерные данные уровня воды
    {"coordinates": "POINT(37.5 56.1)", "level": 152},
    {"coordinates": "POINT(37.5 56.1)", "level": 148},
    {"coordinates": "POINT(37.5 56.1)", "level": 151}
]

# Добавление маркеров наблюдательных пунктов на карту
for obs in observations:
    point = wkt.loads(obs["coordinates"])
    folium.Marker([point.y, point.x], popup=f"Уровень воды: {obs['level']} см").add_to(m)

# Сохранение карты в файл
m.save("26.html")