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

# Пример данных о потреблении воды и уровне воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2023-01-01', 'value': 100},
    {'date': '2023-02-01', 'value': 120},
    {'date': '2023-03-01', 'value': 115},
    {'date': '2023-04-01', 'value': 130},
    {'date': '2023-05-01', 'value': 125}
]

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {'date': '2023-01-01', 'value': 10},
    {'date': '2023-02-01', 'value': 15},
    {'date': '2023-03-01', 'value': 12},
    {'date': '2023-04-01', 'value': 18},
    {'date': '2023-05-01', 'value': 16}
]

# Прогнозирование расхода воды на следующий месяц
from sklearn.linear_model import LinearRegression

# Преобразование данных в массивы numpy
consumption_dates = [int(date.split('-')[1]) for date in water_consumption_data]
consumption_values = [data['value'] for data in water_consumption_data]

level_dates = [int(date.split('-')[1]) for date in water_level_data]
level_values = [data['value'] for data in water_level_data]

# Создание модели линейной регрессии для потребления воды
consumption_model = LinearRegression()
consumption_model.fit(np.array(consumption_dates).reshape(-1, 1), np.array(consumption_values))

# Создание модели линейной регрессии для уровня воды
level_model = LinearRegression()
level_model.fit(np.array(level_dates).reshape(-1, 1), np.array(level_values))

# Прогнозирование расхода воды на следующий месяц (предполагаемый месяц - следующий после последнего)
next_month_consumption = consumption_model.predict([[consumption_dates[-1] + 1]])
print(f"Прогнозируемый расход воды в реке Shilik River на следующий месяц: {next_month_consumption[0]}")

# Сохранение карты
m.save("47.html")