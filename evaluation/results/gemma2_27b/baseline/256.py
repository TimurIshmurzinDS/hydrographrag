import pandas as pd
import folium

# Загрузка данных о составе воды
water_data = pd.read_csv("talgar_water_composition.csv")

# Загрузка рецептов
recipes = pd.read_csv("recipes.csv")

# Функция для поиска подходящих рецептов
def find_recipes(ingredients):
    matching_recipes = recipes[recipes["ingredients"].isin(ingredients)]
    return matching_recipes

# Поиск рецептов, где вода может заменить один из ингредиентов
suitable_recipes = find_recipes(["salt"])

# Создание карты
m = folium.Map(location=[43.1500, 76.8000], zoom_start=12)

folium.Marker(location=[43.1500, 76.8000], popup="River Talgar").add_to(m)

# Сохранение карты
m.save("256.html")

print(suitable_recipes)