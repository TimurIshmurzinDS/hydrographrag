import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import folium

# Загрузите геоданные реки Талгар и Юпитера
talgar = gpd.read_file('talgar.shp')
jupiter = gpd.read_file('jupiter.shp')

# Выберите координаты точек для расчета расстояния
talgar_point = Point(talgar.geometry.x, talgar.geometry.y)
jupiter_point = Point(jupiter.geometry.x, jupiter.geometry.y)

# Расчет расстояния между рекой Талгар и Юпитером
distance = geodesic(talgar_point, jupiter_point).km

# Список ингредиентов коктейля с соответствующими расстояниями
cocktail_ingredients = {
    'Водка': 0,
    'Гиннес': 50,
    'Маргарита': 100,
    'Кока-кола': 150,
    'Абсент': 200
}

# Выберите ингредиенты в зависимости от расстояния
if distance <= cocktail_ingredients['Водка']:
    selected_ingredient = 'Водка'
elif cocktail_ingredients['Гиннес'] < distance <= cocktail_ingredients['Маргарита']:
    selected_ingredient = 'Гиннес'
elif cocktail_ingredients['Маргарита'] < distance <= cocktail_ingredients['Кока-кола']:
    selected_ingredient = 'Маргарита'
else:
    selected_ingredient = 'Абсент'

# Визуализация местоположения реки Талгар и Юпитера на карте
m = folium.Map(location=[talgar_point.y, talgar_point.x], zoom_start=13)
folium.Marker([talgar_point.y, talgar_point.x], popup='Река Талгар').add_to(m)
folium.Marker([jupiter_point.y, jupiter_point.x], popup='Юпитер').add_to(m)

# Добавьте рецепт коктейля на карту
recipe_text = f'Рецепт коктейля: {selected_ingredient}'
folium.Marker([(talgar_point.y + jupiter_point.y) / 2, (talgar_point.x + jupiter_point.x) / 2], popup=recipe_text).add_to(m)

# Сохраните финальную карту как "249.html"
m.save("249.html")