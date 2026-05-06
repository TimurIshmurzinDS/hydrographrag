import folium
from folium.plugins import MarkerCluster

# Пример данных о местах сбора и обработки ила из реки Караой
data = [
    {"name": "Место 1", "lat": 40.7128, "lon": -74.0060},
    {"name": "Место 2", "lat": 39.9522, "lon": -75.1639},
    {"name": "Место 3", "lat": 41.8781, "lon": -87.6298}
]

# Создание карты
m = folium.Map(location=[data[0]['lat'], data[0]['lon']], zoom_start=5)

# Добавление маркеров на карте
marker_cluster = MarkerCluster()
for item in data:
    marker_cluster.add_child(folium.Marker([item['lat'], item['lon']], popup=item['name']))

m.add_child(marker_cluster)

# Сохранение карты в файл
m.save("260.html")