import folium
from shapely.geometry import LineString

# Длина рек в километрах
length_byzhy = 150  # примерная длина Byzhy River
length_lepsy = 200   # примерная длина Lepsy River

# Оценка доступности воды (примерные значения)
water_supply_byzhy = 100  # примерное количество доступной воды в Byzhy River в кубических метрах в день
water_supply_lepsy = 150   # примерное количество доступной воды в Lepsy River в кубических метрах в день

# Потребность животноводства (примерные значения)
livestock_water_demand_byzhy = 80  # примерная потребность животноводства в Byzhy River в кубических метрах в день
livestock_water_demand_lepsy = 120   # примерная потребность животноводства в Lepsy River в кубических метрах в день

# Сравнение доступности и потребности
availability_byzhy = water_supply_byzhy / livestock_water_demand_byzhy
availability_lepsy = water_supply_lepsy / livestock_water_demand_lepsy

print(f"Доступность воды в Byzhy River для животноводства: {availability_byzhy:.2f} дней")
print(f"Доступность воды в Lepsy River для животноводства: {availability_lepsy:.2f} дней")

# Создание карты с использованием folium
m = folium.Map(location=[50, 30], zoom_start=6)

# Добавление линий рек на карту
byzhy_line = LineString([(49.5, 31), (50.5, 32)])  # примерные координаты для Byzhy River
lepsy_line = LineString([(51, 30), (52, 31)])    # примерные координаты для Lepsy River

folium.PolyLine(byzhy_line.coords, color='blue', weight=2.5, opacity=1).add_to(m)
folium.PolyLine(lepsy_line.coords, color='red', weight=2.5, opacity=1).add_to(m)

# Добавление меток с информацией о доступности воды
folium.Marker(byzhy_line.centroid.coords[0], popup=f"Доступность воды в Byzhy River: {availability_byzhy:.2f} дней", icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(lepsy_line.centroid.coords[0], popup=f"Доступность воды в Lepsy River: {availability_lepsy:.2f} дней", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("109.html")