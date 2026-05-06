import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Батарейка
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
coordinates = [
    {"name": "Observation Point", "geometry": wkt.loads("POINT(37.618423 55.755814)")}  # Примерные координаты, заменить на реальные данные
]

# Добавление точек наблюдения на карту
for coord in coordinates:
    folium.Marker(
        location=[coord['geometry'].y, coord['geometry'].x],
        popup=coord['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("220.html")