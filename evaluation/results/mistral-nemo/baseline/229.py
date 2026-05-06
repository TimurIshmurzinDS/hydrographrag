import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Подготовка данных
river_height_data = pd.read_csv('river_height_data.csv')
ingredient_locations = pd.read_csv('ingredient_locations.csv')

# 2. Анализ риска наводнения
river_gdf = gpd.GeoDataFrame(river_height_data, geometry=gpd.points_from_xy(river_height_data['longitude'], river_height_data['latitude']))
river_gdf['risk'] = pd.cut(river_gdf['height'], bins=[0, 5, 10, float('inf')], labels=['Низкий', 'Средний', 'Высокий'])

# 3. Определение доступности ингредиентов
ingredient_gdf = gpd.GeoDataFrame(ingredient_locations, geometry=gpd.points_from_xy(ingredient_locations['longitude'], ingredient_locations['latitude']))
available_ingredients = ingredient_gdf[ingredient_gdf['availability'] == 'Доступно']

# 4. Создание рецепта борща
recipe_ingredients = available_ingredients.sample(n=7) # Выбираем случайные 7 ингредиентов для рецепта
recipe = "Рецепт борща: " + ", ".join(recipe_ingredients['ingredient']) + "."

# 5. Визуализация результатов
m = folium.Map(location=[river_gdf['latitude'].mean(), river_height_data['longitude'].mean()], zoom_start=8)

# Зоны высокого риска наводнения
high_risk_zones = river_gdf[river_gdf['risk'] == 'Высокий']
folium.GeoJson(high_risk_zones[['geometry', 'risk']].to_json(), style_function=lambda x, yz, z: {'fillColor': 'red'}).add_to(m)

# Места, где можно достать ингредиенты для борща
ingredient_locations_gdf = gpd.GeoDataFrame(available_ingredients, geometry=gpd.points_from_xy(available_ingredients['longitude'], available_ingredients['latitude']))
folium.GeoJson(ingredient_locations_gdf[['geometry', 'ingredient']].to_json(), style_function=lambda x, yz, z: {'fillColor': 'green'}).add_to(m)

# Рецепт борща
recipe_popup = folium.Popup(recipe, max_width=300)
folium.Marker([available_ingredients['latitude'].mean(), available_ingredients['longitude'].mean()], popup=recipe_popup).add_to(m)

m.save("229.html")