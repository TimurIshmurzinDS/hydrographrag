import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Фиктивные данные о уровне воды для демонстрации
water_level_data = [
    {'river': 'Aksu River', 'value': 150, 'date': '2023-10-01'},
    {'river': 'Byzhy River', 'value': None, 'date': None}
]

# Добавление данных о уровне воды на карту
for data in water_level_data:
    if data['value'] is not None and data['date'] is not None:
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=f"Река: {data['river']}<br>Уровень воды: {data['value']} м<br>Дата: {data['date']}",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)
    else:
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=f"Река: {data['river']}<br>Датчики неисправны",
            icon=folium.Icon(color='red', icon='warning-sign')
        ).add_to(m)

# Сохранение карты
m.save("65.html")