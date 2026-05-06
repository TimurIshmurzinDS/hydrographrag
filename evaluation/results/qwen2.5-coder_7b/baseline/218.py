import folium
from folium.plugins import MeasureControl

# Координаты Baskan River (пример)
baskan_river_coords = [
    (43.0528, 76.9167),  # Примерная координата начала ручья
    (43.0530, 76.9170),
    (43.0532, 76.9175),
    (43.0535, 76.9180)
]

# Создание карты
m = folium.Map(location=[43.0528, 76.9167], zoom_start=15)

# Добавление измерителя расстояний на карту
MeasureControl().add_to(m)

# Добавление точек с измеренными гравитациями (пример)
gravitational_measurements = {
    'Point 1': {'lat': 43.0528, 'lon': 76.9167, 'gravity': 9.81},
    'Point 2': {'lat': 43.0530, 'lon': 76.9170, 'gravity': 9.82},
    'Point 3': {'lat': 43.0532, 'lon': 76.9175, 'gravity': 9.83},
    'Point 4': {'lat': 43.0535, 'lon': 76.9180, 'gravity': 9.84}
}

# Добавление маркеров с измеренными гравитациями на карту
for point, data in gravitational_measurements.items():
    folium.Marker(
        location=[data['lat'], data['lon']],
        popup=f"{point}: Гравитация = {data['gravity']} м/с^2",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("218.html")