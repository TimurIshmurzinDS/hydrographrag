import folium
from folium.plugins import HeatMap

# Пример данных: координаты угодий и их потребление воды (в литрах)
fields_data = [
    {'lat': 54.123, 'lon': 67.890, 'water_consumption': 1000},
    {'lat': 54.124, 'lon': 67.891, 'water_consumption': 1500},
    # Добавьте больше данных по угодьям
]

# Создание карты
m = folium.Map(location=[54.123, 67.890], zoom_start=12)

# Добавление точек с потреблением воды
for field in fields_data:
    folium.Marker(
        location=[field['lat'], field['lon']],
        popup=f"Угодье: {field['water_consumption']} л/день",
        icon=folium.Icon(color='red', icon='drop')
    ).add_to(m)

# Добавление теплового картографа для визуализации плотности потребления воды
heat_data = [[field['lat'], field['lon'], field['water_consumption']] for field in fields_data]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("190.html")