import folium
from geopandas import GeoDataFrame, Point

# Географические координаты реки Аксу (примерные данные)
axus_coordinates = {
    'latitude': 18.5,
    'longitude': -77.0
}

# Создание геодатафрейма для реки Аксу
axus_point = Point(axus_coordinates['longitude'], axus_coordinates['latitude'])
axus_gdf = GeoDataFrame(geometry=[axus_point])

# Создание карты Марса
m = folium.Map(location=[axus_coordinates['latitude'], axus_coordinates['longitude']], zoom_start=5)

# Добавление точки реки Аксу на карту
folium.Marker(
    location=[axus_coordinates['latitude'], axus_coordinates['longitude']],
    popup='Река Аксу',
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Определение доступности мест для строительства (примерные данные)
buildings = [
    {'name': 'База 1', 'latitude': 18.6, 'longitude': -77.2},
    {'name': 'Станция 1', 'latitude': 18.4, 'longitude': -76.9}
]

# Добавление точек для строительства на карту
for building in buildings:
    folium.Marker(
        location=[building['latitude'], building['longitude']],
        popup=building['name'],
        icon=folium.Icon(color='green', icon='home')
    ).add_to(m)

# Сохранение карты в файл
m.save("248.html")