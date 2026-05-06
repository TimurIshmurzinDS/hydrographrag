import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты наблюдательных пунктов (примерные данные)
observations = [
    {"name": "Observation 1", "coordinates": wkt.loads("POINT(37.5 56.8)")},
    {"name": "Observation 2", "coordinates": wkt.loads("POINT(37.6 56.9)")},
    {"name": "Observation 3", "coordinates": wkt.loads("POINT(37.7 57.0)")}
]

# Добавление маркеров на карту для наблюдательных пунктов
for obs in observations:
    folium.Marker(
        location=[obs["coordinates"].y, obs["coordinates"].x],
        popup=obs["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("68.html")