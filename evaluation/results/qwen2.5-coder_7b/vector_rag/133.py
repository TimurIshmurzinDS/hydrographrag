import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о текущем уровне воды вDos River и исторических данных дляKurty River
current_water_level_dos = 150  # мм
historical_water_levels_kurty = [140, 145, 150, 155, 160]  # мм

# Добавление маркера для текущего уровня воды вDos River
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Текущий уровень воды в Dos River: {current_water_level_dos} мм",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Добавление маркера для среднего уровня воды вKurty River
mean_historical_water_level_kurty = sum(historical_water_levels_kurty) / len(historical_water_levels_kurty)
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Средний уровень воды в Kurty River: {mean_historical_water_level_kurty} мм",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("133.html")