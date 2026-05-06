import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных текущего расхода воды (замените на реальные данные)
current_consumption = {
    "Water_consumption_Value": 150,
    "Unit": "m³s"
}

# Пример исторических данных паводка (замените на реальные данные)
historical_data = [
    {"Date_water_level_Value": "2022-03-01", "Water_consumption_Valuem³s": 200},
    {"Date_water_level_Value": "2022-04-01", "Water_consumption_Valuem³s": 180},
    {"Date_water_level_Value": "2022-05-01", "Water_consumption_Valuem³s": 160}
]

# Добавление точек на карте для текущего расхода и исторических данных
folium.Marker([centroid.y, centroid.x], popup=f"Текущий расход: {current_consumption['Water_consumption_Value']} {current_consumption['Unit']}", icon=folium.Icon(color='red')).add_to(m)
for data in historical_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Исторический расход: {data['Water_consumption_Valuem³s']} m³s на {data['Date_water_level_Value']}", icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("87.html")