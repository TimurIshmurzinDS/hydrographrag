import folium
from folium.plugins import MarkerCluster

# Пример данных о уровне воды (замените на реальные данные)
water_levels = {
    "Ili River": {"level": 120, "latitude": 43.6589, "longitude": 76.2456},
    "Karatal River": {"level": 115, "latitude": 43.7890, "longitude": 76.3456}
}

# Создание карты
m = folium.Map(location=[43.72, 76.28], zoom_start=10)

# Добавление маркеров с уровнями воды
marker_cluster = MarkerCluster().add_to(m)
for river, data in water_levels.items():
    folium.Marker(
        location=[data["latitude"], data["longitude"]],
        popup=f"{river}: {data['level']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("9.html")

print("Карта сохранена как 9.html")