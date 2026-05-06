import folium
from folium.plugins import MarkerCluster

# Пример данных: словарь с координатами датчиков и их статусом
sensor_data = {
    "Или_1": {"lat": 43.05, "lon": 76.25, "status": "исправный"},
    "Или_2": {"lat": 43.10, "lon": 76.30, "status": "неисправный"},
    "Каратал_1": {"lat": 42.95, "lon": 76.15, "status": "исправный"},
    "Каратал_2": {"lat": 42.85, "lon": 76.05, "status": "неисправный"}
}

# Создание карты
m = folium.Map(location=[43.0, 76.1], zoom_start=10)

# Создание маркера для каждой точки
marker_cluster = MarkerCluster()

for sensor_id, data in sensor_data.items():
    if "Или" in sensor_id or "Каратал" in sensor_id:
        folium.Marker(
            location=[data["lat"], data["lon"]],
            popup=f"{sensor_id}: {data['status']}",
            icon=folium.Icon(color="red" if data["status"] == "неисправный" else "green")
        ).add_to(marker_cluster)

# Добавление маркера кластеров на карту
marker_cluster.add_to(m)

# Сохранение карты в файл
m.save("137.html")

print("Карта сохранена как 137.html")