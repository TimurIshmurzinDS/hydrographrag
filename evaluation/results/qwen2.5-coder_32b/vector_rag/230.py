import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Осек
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты folium с центром в бассейне реки Осек
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание синтетических данных о точках наблюдений (координаты в формате WKT)
observations = [
    {"geometry": wkt.loads("POINT(37.5 56.1)"), "value": 1.0},
    {"geometry": wkt.loads("POINT(37.5 56.2)"), "value": 1.1},
    {"geometry": wkt.loads("POINT(37.4 56.1)"), "value": 1.2},
    {"geometry": wkt.loads("POINT(37.4 56.2)"), "value": 1.3}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs["geometry"].y, obs["geometry"].x], popup=f"Value: {obs['value']}").add_to(m)

# Сохранение карты в файл
m.save("230.html")