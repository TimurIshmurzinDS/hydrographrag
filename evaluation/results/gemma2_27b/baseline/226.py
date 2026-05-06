import folium

# Загрузить данные о уровне паводка реки Шарын (заменить на реальные данные)
level_data = [
    (45.123, 60.234, 2.5),  # Координаты и уровень воды
    (45.234, 60.345, 3.0),
]

# Создать карту с Folium
m = folium.Map(location=[45.2, 60.2], zoom_start=12)

# Добавить точки данных о уровне паводка на карту
for coords, level in level_data:
    folium.Marker(location=coords, popup=f"Уровень воды: {level}").add_to(m)

# Сохранить карту в HTML файл
m.save("226.html")

# Пример адаптации рецепта (необходимо заменить на реальную модель)
def adapt_recipe(water_level):
    flour = 200  # стандартное количество муки
    if water_level > 3:
        flour += 50 # увеличить количество муки при высоком уровне паводка

print("Рецепт адаптирован к уровню воды:", level_data)