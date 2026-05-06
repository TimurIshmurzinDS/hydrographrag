python
import folium

# Загрузка данных о рецептах
recipes_before = [
    {"название": "хлеб", "ингредиенты": ["мука", "вода"]},
    {"название": "булочки", "ингредиенты": ["мука", "сахар", "яйца"]}
]

recipes_after = [
    {"название": "хлеб", "ингредиенты": ["мука", "вода", "дрожжи"]},
    {"название": "булочки", "ингредиенты": ["мука", "сахар", "яйца", "масло"]}
]

# Сравнение рецептов
changed_recipes = []
for recipe_before in recipes_before:
    found = False
    for recipe_after in recipes_after:
        if recipe_before["название"] == recipe_after["название"]:
            if set(recipe_before["ингредиенты"]) != set(recipe_after["ингредиенты"]):
                changed_recipes.append({"название": recipe_before["название"], "изменения": list(set(recipe_after["ингредиенты"]) - set(recipe_before["ингредиенты"]))})
            found = True
    if not found:
        changed_recipes.append({"название": recipe_before["название"], "изменения": ["не найдено"]})

# Вывод результатов
print("Измененные рецепты:")
for changed_recipe in changed_recipes:
    print(f"{changed_recipe['название']}: {changed_recipe['изменения']}")

# Визуализация (необязательно)
m = folium.Map()
for recipe in recipes_after:
    folium.Marker(location=[43.0, 78.0], popup=f"{recipe['название']}").add_to(m)

m.save("273.html")