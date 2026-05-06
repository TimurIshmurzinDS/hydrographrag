import folium
import numpy as np
from shapely.geometry import LineString

def calculate_sinuosity(coords):
    """Вычисляет индекс извилистости русла."""
    line = LineString(coords)
    actual_length = line.length
    straight_length = np.sqrt((coords[-1][0] - coords[0][0])**2 + (coords[-1][1] - coords[0][1])**2)
    return actual_length / straight_length if straight_length != 0 else 1

def generate_recipe(sinuosity, length_km):
    """Преобразует топографические данные в рецепт соуса."""
    # База зависит от длины реки
    base_volume = round(length_km / 100, 2) 
    
    recipe = {
        "base": "Оливковое масло и сливки" if sinuosity < 1.5 else "Томатная основа с копченым маслом",
        "complexity": "Простой",
        "ingredients": [],
        "notes": ""
    }

    # Сложность вкуса от извилистости
    if sinuosity > 2.0:
        recipe["complexity"] = "Экзотический и многогранный"
        recipe["ingredients"] = ["Копченая паприка", "Зира", "Чеснок", "Лимонный сок", "Мед"]
    elif sinuosity > 1.3:
        recipe["complexity"] = "Сбалансированный"
        recipe["ingredients"] = ["Черный перец", "Горчица", "Яблочный уксус"]
    else:
        recipe["complexity"] = "Минималистичный"
        recipe["ingredients"] = ["Морская соль", "Сухая зелень"]

    # Добавление 'остроты' за счет анализа меандров (условно)
    if sinuosity > 1.7:
        recipe["notes"] = "Добавьте щепотку кайенского перца, чтобы подчеркнуть резкие повороты русла."
    else:
        recipe["notes"] = "Соус должен быть мягким, как плавное течение реки."

    return recipe, base_volume

# Координаты русла реки Дос (упрощенная аппроксимация для демонстрации GIS-логики)
# В реальном сценарии здесь будет загрузка GeoJSON или Shapefile
dos_river_coords = [
    (68.5, 52.1), (68.6, 52.2), (68.8, 52.1), (68.9, 52.3), 
    (69.1, 52.2), (69.2, 52.4), (69.4, 52.3), (69.5, 52.5),
    (69.7, 52.4), (69.8, 52.6), (70.0, 52.5)
]

# 1. Анализ топографии
sinuosity_index = calculate_sinuosity(dos_river_coords)
# Условно считаем длину в км на основе координат
approx_length = len(dos_river_coords) * 15 

# 2. Генерация рецепта
recipe, volume = generate_recipe(sinuosity_index, approx_length)

# Вывод рецепта в консоль
print("--- РЕЦЕПТ СОУСА 'ТОПОГРАФИЯ РЕКИ ДОС' ---")
print(f"Анализ русла: Индекс извилистости = {sinuosity_index:.2f}")
print(f"Вкусовой профиль: {recipe['complexity']}")
print(f"Основа ({volume} л): {recipe['base']}")
print(f"Ингредиенты: {', '.join(recipe['ingredients'])}")
print(f"Шеф-повар GIS отмечает: {recipe['notes']}")
print("------------------------------------------")

# 3. Визуализация на карте
m = folium.Map(location=[52.3, 69.2], zoom_start=7, tiles="CartoDB positron")

# Рисуем русло реки
folium.PolyLine(
    dos_river_coords, 
    color="blue", 
    weight=4, 
    opacity=0.8, 
    tooltip="Русло реки Дос"
).add_to(m)

# Добавляем маркеры истока и устья
folium.Marker(dos_river_coords[0], popup="Исток", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(dos_river_coords[-1], popup="Устье", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("244.html")