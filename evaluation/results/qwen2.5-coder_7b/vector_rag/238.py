import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат наблюдений (если они есть)
observations = [
    {"id": "1", "time": "2023-04-01T12:00:00Z", "type": "Уровень воды", "value": 5.2, "coordinates": wkt.loads("POINT(10.0 20.0)")},
    {"id": "2", "time": "2023-04-01T13:00:00Z", "type": "Скорость течения", "value": 2.5, "coordinates": wkt.loads("POINT(10.1 20.1)")},
    {"id": "3", "time": "2023-04-01T14:00:00Z", "type": "Уровень воды", "value": 5.5, "coordinates": wkt.loads("POINT(10.2 20.2)")},
    {"id": "4", "time": "2023-04-01T15:00:00Z", "type": "Скорость течения", "value": 2.8, "coordinates": wkt.loads("POINT(10.3 20.3)")},
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs['coordinates'].y, obs['coordinates'].x], popup=f"ID: {obs['id']}, Time: {obs['time']}, Type: {obs['type']}, Value: {obs['value']}").add_to(m)

# Сохранение карты
m.save("238.html")