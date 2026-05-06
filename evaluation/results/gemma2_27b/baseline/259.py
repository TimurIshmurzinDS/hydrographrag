import folium

# Данные о реке (пример)
river_mouth = [53.2167, 80.9167]  # Координаты устья реки Баскан
average_flow = 100 # м³/с (пример)

# Данные о космическом корабле (пример)
cooling_water_needed = 1000 # литры

# Расчет доступности воды
available_water = average_flow * 86400 * 1000  # м³ -> литры в сутки

if available_water >= cooling_water_needed:
    print("Достаточно воды для охлаждения двигателей.")
else:
    print("Недостаточно воды для охлаждения двигателей.")

# Визуализация на карте
m = folium.Map(location=river_mouth, zoom_start=10)
folium.Marker(location=river_mouth, popup="Устье реки Баскан").add_to(m)
m.save("259.html")