import folium
from folium.plugins import FastMarkerCluster

# Пример данных о местоположении рек и их текущих уровнях воды
reaches = {
    "Lepsy River": {"lat": 51.234, "lon": 67.890, "current_level": 100},
    "Sarykan River": {"lat": 52.345, "lon": 68.901, "current_level": 100}
}

# Пример данных о типах растений и животных в реках
flora_fauna = {
    "Lepsy River": ["Fish", "Water lilies", "Reeds"],
    "Sarykan River": ["Turtles", "Aquatic birds", "Crayfish"]
}

# Создание карты
m = folium.Map(location=[51.74, 68.39], zoom_start=10)

# Добавление маркеров для каждой реки с текущим уровнем воды
for reach_name, data in reaches.items():
    folium.Marker(
        location=[data["lat"], data["lon"]],
        popup=f"{reach_name} - Current Level: {data['current_level']}%",
        icon=folium.Icon(color='blue', icon='water')
    ).add_to(m)

# Добавление маркеров для типов растений и животных
for reach_name, species in flora_fauna.items():
    for sp in species:
        folium.Marker(
            location=[reaches[reach_name]["lat"], reaches[reach_name]["lon"]],
            popup=f"{sp} in {reach_name}",
            icon=folium.Icon(color='green' if 'Fish' in sp else 'red')
        ).add_to(m)

# Сохранение карты
m.save("113.html")