import folium
from folium.plugins import FloatImage

# Пример данных: текущий уровень воды реки Баянколь (в метрах)
current_water_level = 10.5  # Замените на реальные данные

# Критические уровни воды для полива
min_water_level_for_irrigation = 8.0
max_water_level_for_irrigation = 12.0

# Расчет потребности в поливе (в метрах кубических)
if current_water_level < min_water_level_for_irrigation:
    water_needed_for_irrigation = 0
elif current_water_level > max_water_level_for_irrigation:
    water_needed_for_irrigation = 0
else:
    # Пример расчета: объем воды для полива пропорционален разнице между текущим уровнем и минимальным уровнем
    water_needed_for_irrigation = (current_water_level - min_water_level_for_irrigation) * 1000000  # в кубических метрах

# Визуализация на карте
m = folium.Map(location=[56.234, 87.912], zoom_start=10)

# Добавление маркера с уровнем воды
folium.Marker(
    location=[56.234, 87.912],
    popup=f"Текущий уровень воды: {current_water_level} м",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Добавление изображения с уровнем воды
water_level_image = f"""
<div style="position: relative; width: 100px; height: 200px;">
    <img src="https://example.com/water_level.png" alt="Water Level" style="width: 100%; height: auto;">
    <div style="position: absolute; bottom: 5px; left: 5px; color: white;">{current_water_level} м</div>
</div>
"""
FloatImage(water_level_image, bottom=10, right=10).add_to(m)

# Сохранение карты
m.save("257.html")

print(f"Потребность в поливе: {water_needed_for_irrigation:.2f} кубических метров")