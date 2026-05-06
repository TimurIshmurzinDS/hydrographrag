import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдений (если есть)
observations = [
    {"name": "Observation Point", "coordinates": wkt.loads("POINT(45.123 60.456)")}  # Пример координат
]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("218.html")