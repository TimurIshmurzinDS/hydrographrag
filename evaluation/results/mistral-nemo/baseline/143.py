import folium

# Создайте пустую карту с центром над Казахстаном
m = folium.Map(location=[50.2796, 68.4137], zoom_start=7)

# Список гидропостов на реке Каратал с их состоянием работоспособности
karatal_hydroposts = [
    {"name": "Гидропост 1", "location": [50.2, 68.4], "status": "рабочий"},
    {"name": "Гидропост 2", "location": [50.3, 68.5], "status": "нерабочий"},
    # Добавьте другие гидропосты на реке Каратал
]

# Список гидропостов на реке Лепсы с их состоянием работоспособности
lepsy_hydroposts = [
    {"name": "Гидропост 1", "location": [50.4, 68.3], "status": "рабочий"},
    {"name": "Гидропост 2", "location": [50.5, 68.4], "status": "нерабочий"},
    # Добавьте другие гидропосты на реке Лепсы
]

# Добавление гидропостов на карту с отметкой их состояния работоспособности
for hydropost in karatal_hydroposts + lepsy_hydroposts:
    folium.Marker(hydropost["location"], popup=f"{hydropost['name']}\nСостояние: {hydropost['status']}").add_to(m)

# Сохранение финальной карты в формате HTML
m.save("143.html")