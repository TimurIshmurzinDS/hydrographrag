import folium
from folium.plugins import MarkerCluster

# Координаты реки Баскан (примерные данные)
bascan_coordinates = [52.0894, 73.5167]

# Создание карты
m = folium.Map(location=bascan_coordinates, zoom_start=13)

# Добавление метки с информацией о реке Баскан
folium.Marker(
    bascan_coordinates,
    popup='Река Баскан',
    icon=folium.Icon(color='blue', icon='water')
).add_to(m)

# Добавление маркера для сбора льда
ice_collection_point = [52.0894, 73.5167]
folium.Marker(
    ice_collection_point,
    popup='Точка сбора льда',
    icon=folium.Icon(color='green', icon='snowflake')
).add_to(m)

# Добавление маркера для охлаждения воды
cooling_point = [52.0894, 73.5167]
folium.Marker(
    cooling_point,
    popup='Точка охлаждения воды',
    icon=folium.Icon(color='red', icon='thermometer')
).add_to(m)

# Сохранение карты
m.save("267.html")