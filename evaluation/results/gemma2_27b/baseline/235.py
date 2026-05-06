import folium

# Замените эти данные на реальные данные о расходе воды реки Или
data = {
    "coordinates": [
        [43.0, 78.0],
        [42.5, 79.0]
    ],
    "flow_rate": [
        100,
        150
    ]
}

# Создаем карту с центром в районе реки Или
m = folium.Map(location=[43.0, 78.0], zoom_start=8)

# Добавляем маркеры на карту, показывающие расход воды
for i in range(len(data["coordinates"])):
    folium.Marker(
        location=data["coordinates"][i],
        popup="Расход: " + str(data["flow_rate"][i]) + " м³/с"
    ).add_to(m)

# Сохраняем карту
m.save("235.html")