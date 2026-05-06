import folium
from folium.plugins import MarkerCluster

# Пример данных о потребности в воде для сельского хозяйства (в литрах)
area_crops = 100000  # Площадь земли под сельском хозяйством в гектарах
water_per_hectare = 5000  # Потребность в воде на единицу площади в литрах

# Пример данных о реках (в литрах в секунду)
flow_kurty = 100000  # Объем воды из Курты в литрах в секунду
flow_lepsy = 50000   # Объем воды из Лепсы в литрах в секунду

# Вычисление общего объема воды, доступного для сельского хозяйства
total_water_available = (flow_kurty + flow_lepsy) * 3600 * 24  # Переводим в литры за день

# Вычисление потребности в воде
water_needed = area_crops * water_per_hectare

# Проверка, достаточно ли объемов воды
if total_water_available >= water_needed:
    print("Достаточно объемов воды для удовлетворения сельскохозяйственного спроса.")
else:
    print("Недостаточно объемов воды для удовлетворения сельскохозяйственного спроса.")

# Визуализация данных на карте
m = folium.Map(location=[54.0, 37.0], zoom_start=6)

# Добавление маркеров для рек
folium.Marker([54.1, 37.2], popup='Курты', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([54.2, 37.3], popup='Лепсы', icon=folium.Icon(color='green')).add_to(m)

# Добавление маркера для сельского хозяйства
folium.Marker([54.15, 37.25], popup='Сельское хозяйство', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("120.html")