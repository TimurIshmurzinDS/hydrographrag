import folium
from folium.plugins import MarkerCluster

# Пример данных: координаты точки, уровень воды и есть ли предупреждение
data = [
    {"lat": 51.2345, "lon": 29.6789, "water_level": 10.5, "alert": False},
    {"lat": 51.2346, "lon": 29.6790, "water_level": 12.0, "alert": True},
    {"lat": 51.2347, "lon": 29.6791, "water_level": 8.0, "alert": False}
]

# Создание карты
m = folium.Map(location=[51.2345, 29.6789], zoom_start=13)

# Группа для маркеров с предупреждениями
alert_cluster = MarkerCluster(name="Предупреждения о высоком уровне воды")

# Добавление маркеров на карту
for item in data:
    if item["alert"]:
        folium.Marker(
            [item["lat"], item["lon"]],
            popup=f"Уровень воды: {item['water_level']} м\nПредупреждение: Да",
            icon=folium.Icon(color="red", icon="warning"),
            tooltip="Предупреждение о высоком уровне воды"
        ).add_to(alert_cluster)
    else:
        folium.Marker(
            [item["lat"], item["lon"]],
            popup=f"Уровень воды: {item['water_level']} м\nПредупреждение: Нет",
            icon=folium.Icon(color="green", icon="check"),
            tooltip="Нормальный уровень воды"
        ).add_to(m)

# Добавление группы маркеров с предупреждениями на карту
alert_cluster.add_to(m)

# Добавление легенды
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("28.html")