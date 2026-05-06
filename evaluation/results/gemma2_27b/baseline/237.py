import folium

# Определение ингредиентов
ingredients = {
    "Водка": "50 мл",
    "Сироп из лимона": "20 мл",
    "Сок из грейпфрута": "100 мл",
    "Газированная вода": "50 мл",
}

# Создание карты
m = folium.Map(location=[43.8, 76.9], zoom_start=12)

# Добавление маркеров для каждого ингредиента
for ingredient, amount in ingredients.items():
    folium.Marker(location=[43.8, 76.9], popup=f"{ingredient}: {amount}", icon=folium.Icon(color="red" if "алко" in ingredient else "green")).add_to(m)

# Сохранение карты
m.save("237.html")