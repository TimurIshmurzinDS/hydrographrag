import folium
from folium.plugins import MarkerCluster

# Пример данных: текущий уровень воды в реке Аягоз и потребность в воде для ирригации
current_water_level = 100  # метров
max_irrigation_demand = 200  # метров

# Расчет дефицита воды
water_deficit = max_irrigation_demand - current_water_level

# Создание карты с использованием folium
m = folium.Map(location=[43.167, 85.167], zoom_start=12)

# Добавление маркера для реки Аягоз
folium.Marker(
    location=[43.167, 85.167],
    popup='Река Аягоз',
    icon=folium.Icon(color='blue', icon='water')
).add_to(m)

# Добавление маркера для дефицита воды
if water_deficit > 0:
    folium.Marker(
        location=[43.167, 85.167],
        popup=f'Дефицит воды: {water_deficit} м',
        icon=folium.Icon(color='red', icon='warning')
    ).add_to(m)
else:
    folium.Marker(
        location=[43.167, 85.167],
        popup='Дефицит воды не обнаружен',
        icon=folium.Icon(color='green', icon='checkmark')
    ).add_to(m)

# Сохранение карты
m.save("35.html")