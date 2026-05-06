import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек наблюдений (WKT)
observations = [
    {"id": "Observation_2264", "geometry": wkt.loads("POINT(35.123 58.456)")},
    {"id": "Observation_2247", "geometry": wkt.loads("POINT(35.234 58.567)")},
    {"id": "Observation_2278", "geometry": wkt.loads("POINT(35.345 58.678)")},
    {"id": "Observation_2248", "geometry": wkt.loads("POINT(35.456 58.789)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['id'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("191.html")