import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: дата и расход воды в реке Shyzhyn River
data = {
    'date': ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', 
             '2018-06-01', '2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', 
             '2018-11-01', '2018-12-01'],
    'flow': [10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Построение временного ряда
df.plot(title='Сезонный расход воды реки Shyzhyn River')

# Прогнозирование с помощью ARIMA
model = ARIMA(df['flow'], order=(5,1,0))
model_fit = model.fit()
forecast = model_fit.forecast(steps=12)

# Визуализация прогноза на карте
m = folium.Map(location=[48.3769, 35.0667], zoom_start=10)  # Координаты примерного местоположения реки

# Добавление данных в GeoJSON формате
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [35.0667, 48.3769]
            },
            "properties": {
                "time": df.index[-1].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": df['flow'].iloc[-1],
                "forecast": forecast[0]
            }
        }
    ]
}

# Добавление прогноза на карту
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("21.html")