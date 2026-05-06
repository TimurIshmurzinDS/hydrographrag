import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на границе ровнин
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнин на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровня воды для реки Lepsy River (замените на реальные данные)
water_level_data = [
    {'date': '2023-01-01', 'value': 5},
    {'date': '2023-02-01', 'value': 6},
    {'date': '2023-03-01', 'value': 7},
    {'date': '2023-04-01', 'value': 8},
    {'date': '2023-05-01', 'value': 9}
]

# Прогнозирование уровней воды (простой пример линейной регрессии)
import numpy as np
from sklearn.linear_model import LinearRegression

dates = np.array([i['date'] for i in water_level_data]).reshape(-1, 1)
values = np.array([i['value'] for i in water_level_data])

model = LinearRegression()
model.fit(dates, values)

# Прогнозирование для следующего сезона
next_season_dates = np.array([[len(water_level_data) + 1], [len(water_level_data) + 2]])
predicted_values = model.predict(next_season_dates)

# Добавление прогнозируемых уровней воды на карту
for date, value in zip(next_season_dates.flatten(), predicted_values):
    folium.Marker([centroid.y, centroid.x], popup=f"Прогнозируемый уровень воды: {value}").add_to(m)

# Сохранение карты
m.save("128.html")