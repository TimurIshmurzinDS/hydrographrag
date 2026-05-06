import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('tokyraun_water_flow.csv', parse_dates=['date'], index_col='date')

# Предварительная обработка данных
data.dropna(inplace=True)

# Создание модели ARIMA
model = ARIMA(data['flow'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование на основе исторических данных
forecast_steps = 365  # Прогноз на год вперед
forecast = model_fit.forecast(steps=forecast_steps)

# Оценка производительности модели (пример)
mse = mean_squared_error(data['flow'][-100:], forecast[:100])
print(f'Mean Squared Error: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[data.index[0].year, data.index[0].month], zoom_start=5)

# Добавление данных о стоке реки Токыраун
tokyraun_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data.index[0].year, data.index[0].month]
            },
            "properties": {
                "time": data.index[0],
                "value": data['flow'][0]
            }
        }
    ]
}

# Добавление прогнозных данных
forecast_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data.index[-1].year + i, data.index[-1].month]
            },
            "properties": {
                "time": data.index[-1] + pd.Timedelta(days=i),
                "value": forecast[i]
            }
        }
        for i in range(forecast_steps)
    ]
}

TimestampedGeoJson(tokyraun_data, period="PT1D", add_last_point=True).add_to(m)
TimestampedGeoJson(forecast_data, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("193.html")