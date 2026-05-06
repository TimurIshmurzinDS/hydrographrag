import folium

# Шаг 1: Подготовка данных
recipes_before = [
    {"name": "Recipe 1", "ingredients": ["flour", "water"], "location": [43.25, 69.20]},
    {"name": "Recipe 2", "ingredients": ["flour", "yeast"], "location": [43.28, 69.22]}
]

recipes_after = [
    {"name": "Recipe 1", "ingredients": ["flour", "water", "salt"], "location": [43.25, 69.20]},
    {"name": "Recipe 2", "ingredients": ["flour", "yeast", "oil"], "location": [43.28, 69.22]}
]

# Шаг 2: Анализ данных
def analyze_recipes(recipes_before, recipes_after):
    changes = []
    for i in range(len(recipes_before)):
        if recipes_before[i]["ingredients"] != recipes_after[i]["ingredients"]:
            changes.append({
                "name": recipes_before[i]["name"],
                "location": recipes_before[i]["location"],
                "changes": list(set(recipes_after[i]["ingredients"]) - set(recipes_before[i]["ingredients"]))
            })
    return changes

changes = analyze_recipes(recipes_before, recipes_after)

# Шаг 3: Визуализация данных
m = folium.Map(location=[43.265, 69.21], zoom_start=10)

for change in changes:
    folium.Marker(change["location"], popup=f"{change['name']}: {', '.join(change['changes'])}").add_to(m)

# Шаг 4: Сохранение карты
m.save("273.html")