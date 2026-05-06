import folium
from folium.plugins import MarkerCluster

# Текущий уровень воды в реке Турген (в метрах)
current_water_level = 10.5

# Потребность в воде для орошения садов (в кубических метрах)
water_needed_for_irrigation = 200000

# Объем воды, который можно получить из реки (в кубических метрах)
volume_of_water_in_river = current_water_level * 100000  # Пример объема на основе текущего уровня и площади реки

# Оценка доступности воды
if volume_of_water_in_river >= water_needed_for_irrigation:
    availability_status = "Достаточно воды для орошения садов"
else:
    availability_status = "Недостаточно воды для полного орошения садов"

# Создание карты
m = folium.Map(location=[54.1967, 83.0233], zoom_start=12)

# Добавление метки с информацией о доступности воды
folium.Marker(
    location=[54.1967, 83.0233],
    popup=f"Текущий уровень воды в реке Турген: {current_water_level} м<br>Доступность воды для орошения садов: {availability_status}",
    icon=folium.Icon(color='green' if availability_status == "Достаточно воды для орошения садов" else 'red')
).add_to(m)

# Сохранение карты
m.save("183.html")