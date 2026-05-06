import geopandas as gpd
import folium

# Загрузка данных о реке
river = gpd.read_file("uzyn_kargaly.shp")

# Расчет средней длины реки
average_length = river.geometry.length.mean()

# Определение уровня жидкости
def liquid_level(length):
    if length < 10:
        return 1
    elif length < 20:
        return 2
    elif length < 30:
        return 3
    elif length < 40:
        return 4
    else:
        return 5

level = liquid_level(average_length)

# Словарь с рецептами коктейлей
cocktails = {
    1: ["Вода", "Лимон"],
    2: ["Водка", "Сок", "Лёд"],
    3: ["Кофе", "Молоко", "Сахар"],
    4: ["Вино", "Сыр", "Грецкие орехи"],
    5: ["Шампанское", "Фрукты", "Ягоды"]
}

# Выбор рецепта по уровню жидкости
recipe = cocktails[level]

# Генерация HTML карты с Folium (необязательно)
m = folium.Map(location=[40, 60], zoom_start=5)
folium.GeoJson("uzyn_kargaly.shp").add_to(m)
m.save("219.html")

# Вывод рецепта
print(f"Ваш коктейль: {', '.join(recipe)}")