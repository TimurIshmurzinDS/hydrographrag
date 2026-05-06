import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о расходе воды (если доступны)
water_consumption_data = [
    {'name': 'Kurty River', 'value': 150, 'unit': 'm³'},
    {'name': 'Tekes River', 'value': 200, 'unit': 'm³'}
]

# Добавление маркеров на карте с данными о расходе воды
for data in water_consumption_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"{data['name']}: {data['value']} {data['unit']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("129.html")