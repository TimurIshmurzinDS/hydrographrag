import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдательных пунктов (если есть)
observations = [
    {"name": "Temirlik village", "coordinates": wkt.loads("POINT(76.9345 42.8123)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs['coordinates'].y, obs['coordinates'].x], popup=obs['name']).add_to(m)

# Сохранение карты
m.save("118.html")