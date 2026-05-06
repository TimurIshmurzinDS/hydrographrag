import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о водных уровнях (замените на реальные данные)
water_level_data = [
    {'date': '2018-01-01', 'value': 50},
    {'date': '2018-02-01', 'value': 60},
    {'date': '2018-03-01', 'value': 70},
    {'date': '2018-04-01', 'value': 80},
    {'date': '2018-05-01', 'value': 90},
    # Добавьте данные за последние 5 лет
]

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(water_level_data)
df['date'] = pd.to_datetime(df['date'])

# Пример простой модели прогнозирования (линейная регрессия)
from sklearn.linear_model import LinearRegression

X = df[['date']]
y = df['value']
model = LinearRegression()
model.fit(X, y)

# Предсказание будущих значений
future_dates = pd.date_range(start=df['date'].max(), periods=30, freq='D')
future_predictions = model.predict(future_dates.values.reshape(-1, 1))

# Визуализация данных и прогнозов
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['value'], label='Исторические данные', marker='o')
plt.plot(future_dates, future_predictions, label='Прогнозы', linestyle='--')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (см)')
plt.title('Прогнозирование уровня паводка для реки Dos River')
plt.legend()
plt.show()

# Сохранение карты
m.save("50.html")