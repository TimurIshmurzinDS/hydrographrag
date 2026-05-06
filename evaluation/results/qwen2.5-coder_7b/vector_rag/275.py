import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинки на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о водных уровнях (замените на реальные данные)
water_level_data = [
    {'date': '2023-01-01', 'value': 5},
    {'date': '2023-02-01', 'value': 6},
    {'date': '2023-03-01', 'value': 7},
    {'date': '2023-04-01', 'value': 8},
    {'date': '2023-05-01', 'value': 9},
    {'date': '2023-06-01', 'value': 10},
    {'date': '2023-07-01', 'value': 11},
    {'date': '2023-08-01', 'value': 12},
    {'date': '2023-09-01', 'value': 13},
    {'date': '2023-10-01', 'value': 14},
    {'date': '2023-11-01', 'value': 15},
    {'date': '2023-12-01', 'value': 16}
]

# Преобразование данных в DataFrame
import pandas as pd
df = pd.DataFrame(water_level_data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Прогнозирование временного ряда с использованием ARIMA
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['value'], order=(5,1,0))
model_fit = model.fit()

# Предсказание будущих значений
forecast_steps = 12
forecast = model_fit.forecast(steps=forecast_steps)

# Добавление предсказанных значений на карту
for i in range(forecast_steps):
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Прогнозируемый уровень воды: {forecast[i]:.2f}",
        icon=folium.Icon(color='red', icon='cloud')
    ).add_to(m)

# Сохранение карты
m.save("275.html")