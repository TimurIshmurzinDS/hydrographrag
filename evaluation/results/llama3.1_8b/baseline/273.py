import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор данных (предположим, что данные хранятся в файле 'recipes.csv')
recipes = pd.read_csv('recipes.csv')

# Анализ данных: определение расстояния до реки Каратал
def distance_to_karatal(lat, lon):
    # Координаты реки Каратал (предположим)
    karatal_lat, karatal_lon = 43.1234, 76.5678
    
    return ((lat - karatal_lat) ** 2 + (lon - karatal_lon) ** 2) ** 0.5

recipes['distance_to_karatal'] = recipes.apply(lambda row: distance_to_karatal(row['latitude'], row['longitude']), axis=1)

# Моделирование: определение влияния реки Каратал на состав рецептов
def model_recipe(recipe):
    # Предположим, что мы используем линейную регрессию для моделирования
    from sklearn.linear_model import LinearRegression
    
    X = recipe[['distance_to_karatal']]
    y = recipe['ingredients']
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model.predict([[recipe['distance_to_karatal']]])

recipes['predicted_ingredients'] = recipes.apply(model_recipe, axis=1)

# Визуализация: карта с распределением рецептов и их составом
m = Map(location=[43.1234, 76.5678], zoom_start=10)
HeatMap(data=list(zip(recipes['latitude'], recipes['longitude'])), radius=20).add_to(m)

for index, row in recipes.iterrows():
    Marker([row['latitude'], row['longitude']], popup=f"Рецепт: {row['name']}").add_to(m)

m.save("273.html")