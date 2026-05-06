import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='2023-06-01', periods=100, freq='D'),
    'flow_rate': np.random.normal(loc=500, scale=100, size=100)  # Примерные данные о расходе воды
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Препроцессинг данных (простой пример)
df['flow_rate'] = df['flow_rate'].clip(lower=0)

# Анализ временных рядов
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(df['flow_rate'], model='additive', period=7)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Построение модели (пример с использованием ARIMA)
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['flow_rate'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

# Визуализация результатов на карте
m = folium.Map(location=[52.4867, 36.9167], zoom_start=10)  # Координаты примера (замените на реальные координаты реки)

# Добавление данных о расходе воды на карте
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [36.9167, 52.4867]  # Координаты примера (замените на реальные координаты реки)
            },
            "properties": {
                "time": df.index[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": df['flow_rate'][0]
            }
        }
    ]
}

TimestampedGeoJson(geojson_data, period='PT1H', add_last_point=True).add_to(m)

# Сохранение карты
m.save("20.html")