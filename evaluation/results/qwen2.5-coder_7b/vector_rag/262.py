import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о ценах на нефть и популяции рыб (замените на реальные данные)
oil_prices = [50, 60, 70, 80, 90]  # Цена на нефть в долларах за баррель
fish_population = [1000, 800, 600, 400, 200]  # Популяция рыб

# Создание DataFrame для анализа
import pandas as pd
data = pd.DataFrame({
    'oil_price': oil_prices,
    'fish_population': fish_population
})

# Простая линейная регрессия
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(data[['oil_price']], data['fish_population'])

# Предсказание популяции рыб на основе текущей цены на нефть
current_oil_price = 75  # Пример текущей цены на нефть
predicted_fish_population = model.predict([[current_oil_price]])

print(f"Предсказанная популяция рыб в реке Бутак при цене на нефть {current_oil_price} долларов за баррель: {predicted_fish_population[0]:.2f}")

# Сохранение карты
m.save("262.html")