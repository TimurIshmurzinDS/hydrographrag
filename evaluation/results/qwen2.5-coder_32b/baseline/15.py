import folium

# Синтетические данные: координаты реки Улкен Алматы и текущий уровень воды (в метрах над уровнем моря)
river_coordinates = [42.8743, 76.9105]  # примерные координаты
water_level = 1200  # синтетический уровень воды в метрах

# Создание карты folium
m = folium.Map(location=river_coordinates, zoom_start=12)

# Добавление маркера с информацией о уровне воды
folium.Marker(
    location=river_coordinates,
    popup=f"Уровень воды: {water_level} м",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Сохранение карты в файл
m.save("15.html")

print(f"Карта сохранена как 15.html с уровнем воды: {water_level} м")