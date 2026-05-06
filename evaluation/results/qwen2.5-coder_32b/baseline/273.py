import pandas as pd
import folium

# Шаг 1: Сбор данных о рецептах хлеба
# Предположим, что у нас есть два CSV файла: historical_recipes.csv и modern_recipes.csv
historical_recipes = pd.read_csv('historical_recipes.csv')
modern_recipes = pd.read_csv('modern_recipes.csv')

# Шаг 2: Геоданные о реке Karatal и регионах производства хлеба
# Предположим, что у нас есть CSV файл с координатами регионов: regions.csv
regions = pd.read_csv('regions.csv')  # Должен содержать столбцы: region_name, latitude, longitude

# Шаг 3: Анализ данных
# Простой пример анализа: сравнение количества ингредиентов в рецептах
historical_ingredient_count = historical_recipes['ingredients'].apply(lambda x: len(x.split(',')))
modern_ingredient_count = modern_recipes['ingredients'].apply(lambda x: len(x.split(',')))

# Пример вывода среднего количества ингредиентов
print(f"Среднее количество ингредиентов в исторических рецептах: {historical_ingredient_count.mean()}")
print(f"Среднее количество ингредиентов в современных рецептах: {modern_ingredient_count.mean()}")

# Шаг 4: Визуализация на карте
m = folium.Map(location=[regions['latitude'].mean(), regions['longitude'].mean()], zoom_start=10)

# Добавление маркеров для регионов производства хлеба
for idx, row in regions.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['region_name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("273.html")