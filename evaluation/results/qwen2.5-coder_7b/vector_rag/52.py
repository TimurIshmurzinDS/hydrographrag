import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных для прогнозирования (замените на реальные данные)
data = [
    {'Water_level_Value': 15, 'Water_Classification': 3, 'Water_consumption_Value': 10},
    {'Water_level_Value': 20, 'Water_Classification': 4, 'Water_consumption_Value': 15},
    {'Water_level_Value': 25, 'Water_Classification': 5, 'Water_consumption_Value': 20}
]

# Прогнозирование стока
predicted_water_levels = []
for row in data:
    predicted_level = 0.5 * row['Water_level_Value'] + 0.3 * row['Water_Classification'] - 0.2 * row['Water_consumption_Value']
    predicted_water_levels.append(predicted_level)

# Добавление прогнозируемых уровней воды на карту
for i, level in enumerate(predicted_water_levels):
    folium.Marker([centroid.y + (i-1)*0.5, centroid.x], popup=f"Predicted Water Level: {level}").add_to(m)

# Сохранение карты
m.save("52.html")