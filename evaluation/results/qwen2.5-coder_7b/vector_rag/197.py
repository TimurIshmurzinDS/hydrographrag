import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроидов shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды и потреблении воды (замените на реальные данные)
water_level_data = [
    {'date': '2023-01-01', 'value': 50},
    {'date': '2023-02-01', 'value': 60},
    {'date': '2023-03-01', 'value': 70},
    # Добавьте больше данных
]

water_consumption_data = [
    {'date': '2023-01-01', 'value': 1000},
    {'date': '2023-02-01', 'value': 1500},
    {'date': '2023-03-01', 'value': 2000},
    # Добавьте больше данных
]

# Пример кода для анализа временных рядов и создания модели прогнозирования (замените на реальный код)
from sklearn.linear_model import LinearRegression
import pandas as pd

# Создание DataFrame из данных о уровне воды
water_level_df = pd.DataFrame(water_level_data)
water_level_df['date'] = pd.to_datetime(water_level_df['date'])
water_level_df.set_index('date', inplace=True)

# Создание модели линейной регрессии для прогнозирования уровня воды
model = LinearRegression()
model.fit(water_level_df.index.values.reshape(-1, 1), water_level_df['value'])

# Прогнозирование уровня воды на следующий сезон
future_dates = pd.date_range(start=water_level_df.index[-1], periods=30, freq='D')
predicted_water_levels = model.predict(future_dates.values.reshape(-1, 1))

# Добавление прогнозов на карту (пример)
for date, level in zip(future_dates, predicted_water_levels):
    folium.Marker([centroid.y, centroid.x], popup=f"Прогнозированное значение уровня воды: {level}").add_to(m)

# Сохранение карты
m.save("197.html")