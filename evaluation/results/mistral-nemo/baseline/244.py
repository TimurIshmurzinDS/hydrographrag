import folium
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Получение данных о топографии русла реки Дос.
river_data = gpd.read_file("river_dos_topography.shp")

# Шаг 2: Анализ данных о рельефе местности.
river_data['elevation'] = river_data['geometry'].apply(lambda x: x.centroid.y)
river_data['slope'] = river_data['geometry'].apply(lambda x: x.tangent)

# Шаг 3: Использование характеристик ландшафта для выбора ингредиентов соуса.
soy_sauce_recipe = {
    'soy_sauce': lambda x: x['elevation'] / 10,
    'sugar': lambda x: (x['elevation'] - x['slope']) / 10,
    'vinegar': lambda x: x['slope'] / 10
}

recipe_data = river_data.apply(lambda row: {k: func(row) for k, func in soy_sauce_recipe.items()}, axis=1)

# Шаг 4: Визуализация результатов на карте с использованием библиотеки `folium`.
m = folium.Map(location=[river_data['geometry'].centroid.y.mean(), river_data['geometry'].centroid.x.mean()], zoom_start=12)

for _, row in recipe_data.iterrows():
    point = Point(row['geometry'].centroid.x, row['geometry'].centroid.y)
    folium.Marker(point, popup=f"Соуса: {row['soy_sauce']}\nСахар: {row['sugar']}\nУксус: {row['vinegar']}").add_to(m)

m.save("244.html")