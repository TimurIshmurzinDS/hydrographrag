import folium
import math

def haversine(coord1, coord2):
    """Вычисляет расстояние между двумя точками в километрах."""
    R = 6371.0  # Радиус Земли
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def generate_cocktail_recipe(river_length, complexity):
    """Генерирует рецепт коктейля на основе параметров реки."""
    # Нормализуем длину реки для объема (например, 1 км = 0.5 мл, макс 150 мл)
    base_volume = min(150, river_length * 0.5)
    # Модификатор зависит от сложности (количества точек/изгибов)
    modifier_volume = min(60, complexity * 2)
    # Топпер заполняет остаток до 300 мл
    topper_volume = 300 - (base_volume + modifier_volume)
    
    recipe = {
        "Название": "Степной Поток (Uzyn Kargaly Spirit)",
        "Ингредиенты": {
            "Степной Джин (База)": f"{round(base_volume, 1)} мл",
            "Лимонный сок (Модификатор извилистости)": f"{round(modifier_volume, 1)} мл",
            "Тоник с ароматом полыни (Топпер)": f"{round(topper_volume, 1)} мл"
        },
        "Инструкция": "Смешать в высоком стакане со льдом, украсить веточкой местной травы."
    }
    return recipe

# 1. Координаты реки Uzyn Kargaly (упрощенная аппроксимация русла)
# В реальном ГИС-проекте здесь был бы GeoJSON или Shapefile
uzyn_kargaly_coords = [
    (50.45, 52.10), (50.48, 52.25), (50.52, 52.40), 
    (50.55, 52.60), (50.58, 52.80), (50.62, 53.00),
    (50.65, 53.20), (50.68, 53.45)
]

# 2. Расчет общей длины реки
total_length = 0
for i in range(len(uzyn_kargaly_coords) - 1):
    total_length += haversine(uzyn_kargaly_coords[i], uzyn_kargaly_coords[i+1])

# 3. Генерация рецепта
complexity = len(uzyn_kargaly_coords)
cocktail = generate_cocktail_recipe(total_length, complexity)

# Вывод рецепта в консоль
print(f"--- {cocktail['Название']} ---")
print(f"Длина реки Uzyn Kargaly: {round(total_length, 2)} км")
for ing, vol in cocktail['Ингредиенты'].items():
    print(f"{ing}: {vol}")
print(f"\n{cocktail['Инструкция']}")

# 4. Визуализация на карте
m = folium.Map(location=[50.55, 52.75], zoom_start=7, tiles="CartoDB positron")

# Рисуем русло реки
folium.PolyLine(
    uzyn_kargaly_coords, 
    color="blue", 
    weight=4, 
    opacity=0.8, 
    tooltip="Uzyn Kargaly River"
).add_to(m)

# Добавляем маркеры начала и конца
folium.Marker(uzyn_kargaly_coords[0], popup="Исток", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(uzyn_kargaly_coords[-1], popup="Устье", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("219.html")