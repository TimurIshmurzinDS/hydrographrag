import folium
from folium.plugins import MarkerCluster

# Пример данных: координаты сенсора и его текущий статус
sensor_data = {
    "latitude": 51.2345,
    "longitude": -0.7890,
    "status": "normal"  # Возможные значения: "normal", "alarm", "warning"
}

# Создание карты
m = folium.Map(location=[sensor_data["latitude"], sensor_data["longitude"]], zoom_start=15)

# Добавление маркера сенсора на карте
marker_cluster = MarkerCluster().add_to(m)
folium.Marker(
    [sensor_data["latitude"], sensor_data["longitude"]],
    popup=f"Sensor Status: {sensor_data['status']}",
    icon=folium.Icon(color="green" if sensor_data["status"] == "normal" else 
                      "red" if sensor_data["status"] == "alarm" else 
                      "orange")
).add_to(marker_cluster)

# Сохранение карты
m.save("6.html")

print("Карта сохранена как 6.html")