import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о паводках и уровнях воды (замените на реальные данные)
pavodka_data = [
    {'date': '2023-04-15', 'water_level': 120},
    {'date': '2023-04-16', 'water_level': 125},
    {'date': '2023-04-17', 'water_level': 130},
    # Добавьте больше данных по необходимости
]

# Визуализация пикового уровня воды на карте
max_water_level = max(pavodka_data, key=lambda x: x['water_level'])
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Пиковый уровень воды: {max_water_level['water_level']} м",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("22.html")