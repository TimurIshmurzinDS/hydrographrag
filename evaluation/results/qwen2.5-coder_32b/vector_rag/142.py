import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек наблюдения (координаты предположительные, так как в контексте нет конкретных данных)
observations = [
    {"name": "1.7 km above the mouth of Kishi Osek River", "coordinates": wkt.loads("POINT(38.25 46.05)")}
]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("142.html")