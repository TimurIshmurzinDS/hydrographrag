import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на границе бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных расхода воды и уровня воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2023-04-01', 'consumption': 500},
    {'date': '2023-04-02', 'consumption': 600},
    {'date': '2023-04-03', 'consumption': 700}
]

water_level_data = [
    {'date': '2023-04-01', 'level': 5},
    {'date': '2023-04-02', 'level': 6},
    {'date': '2023-04-03', 'level': 7}
]

# Визуализация данных расхода воды и уровня воды
for data in water_consumption_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Расход воды: {data['consumption']} м³", icon=folium.Icon(color='red')).add_to(m)

for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды: {data['level']} м", icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("27.html")