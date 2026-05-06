import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы ручья из shapefile файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре массы границы ручья
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка слоев для отображения информации о реках и уровнях воды
layers = []

# Добавление информации о реке Коктал
kakatal_river = {
    "name": "Коктал",
    "level": 0.2,
    "position": "0.2 km above the confluence with Osek River"
}
layers.append(kakatal_river)

# Добавление информации о реке Каратал
karatal_river = {
    "name": "Каратал",
    "level": None,  # Уровень воды не указан в контексте
    "position": None  # Положение относительно других ручьев не указано в контексте
}
layers.append(karatal_river)

# Добавление слоев на карту
for layer in layers:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Река: {layer['name']}\nУровень воды: {layer['level']} km\nПозиция: {layer['position']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты в файл
m.save("239.html")