import folium
from folium.plugins import MarkerCluster

# Пример данных о координатах оборудования и его состоянии
equipment_data = [
    {"name": "Оборудование 1", "coordinates": [42.8500, 74.6000], "status": "Работает"},
    {"name": "Оборудование 2", "coordinates": [42.8550, 74.6050], "status": "Не работает"},
    {"name": "Оборудование 3", "coordinates": [42.8600, 74.6100], "status": "Работает"},
    {"name": "Оборудование 4", "coordinates": [42.8525, 74.6025], "status": "Не работает"}
]

# Создание карты с центром в средней точке оборудования
map_center = [sum(coord[0] for coord in [eq["coordinates"] for eq in equipment_data]) / len(equipment_data),
              sum(coord[1] for coord in [eq["coordinates"] for eq in equipment_data]) / len(equipment_data)]

m = folium.Map(location=map_center, zoom_start=12)

# Создание кластера маркеров
marker_cluster = MarkerCluster().add_to(m)

# Добавление маркеров на карту с учетом состояния оборудования
for eq in equipment_data:
    if eq["status"] == "Работает":
        icon_color = 'green'
    else:
        icon_color = 'red'
    
    folium.Marker(
        location=eq["coordinates"],
        popup=f"{eq['name']}: {eq['status']}",
        icon=folium.Icon(color=icon_color)
    ).add_to(marker_cluster)

# Сохранение карты в файл
m.save("66.html")