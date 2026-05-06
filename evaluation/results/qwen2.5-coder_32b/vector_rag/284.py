import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=5)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример списка наблюдений (координаты в формате WKT)
observations = [
    {"id": "Observation_2200", "wkt": "POINT(137.446 -30.594)", "date_water_level_value": "2020-01-01 12:00:00, 1.2"},
    {"id": "Observation_0", "wkt": "POINT(138.446 -31.594)", "date_water_level_value": "2020-02-01 12:00:00, 1.3"},
    {"id": "Observation_1", "wkt": "POINT(139.446 -32.594)", "date_water_level_value": "2020-03-01 12:00:00, 1.4"},
    {"id": "Observation_2", "wkt": "POINT(140.446 -33.594)", "date_water_level_value": "2020-04-01 12:00:00, 1.5"}
]

# Добавление маркеров наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker([point.y, point.x], popup=f"{obs['id']}: {obs['date_water_level_value']}").add_to(m)

# Сохранение карты в файл
m.save("284.html")