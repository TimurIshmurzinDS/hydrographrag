import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import folium
from folium.plugins import TimestampedGeoJson

# Сбор данных (пример: загрузка из CSV файла)
data = pd.read_csv('bayankol_water_level.csv', parse_dates=['date'], index_col='date')

# Обработка данных
data['water_level'] = data['water_level'].astype(float)

# Анализ временных рядов
model = ARIMA(data['water_level'], order=(5,1,0))
results = model.fit()

# Прогнозирование колебаний уровня воды на следующие 7 дней
forecast = results.get_forecast(steps=7)
forecast_ci = forecast.conf_int()

# Создание карты с прогнозами
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление данных о колебаниях уровня воды на карте
water_level_data = []
for index, row in data.iterrows():
    water_level_data.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": index.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "water_level": row['water_level']
        }
    })

# Добавление прогнозов на карту
forecast_data = []
for i, forecast_value in enumerate(forecast.predicted_mean):
    forecast_time = data.index[-1] + pd.Timedelta(days=i+1)
    forecast_data.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [data['longitude'].mean(), data['latitude'].mean()]
        },
        "properties": {
            "time": forecast_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "water_level": forecast_value
        }
    })

TimestampedGeoJson(water_level_data, period="PT1H", add_last_point=True).add_to(m)
TimestampedGeoJson(forecast_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("215.html")