import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import folium

# Сбор и подготовка данных
data = {
    'Дата': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01'],
    'Волна миграции': [100, 120, 110, 130, 140]
}
df = pd.DataFrame(data)
df['Дата'] = pd.to_datetime(df['Дата'])
df.set_index('Дата', inplace=True)

# Анализ данных
print(df.describe())

# Моделирование
model = ARIMA(df, order=(5,1,0))
model_fit = model.fit()

# Оценка модели
forecast_steps = 3
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)
mse = mean_squared_error(df[-forecast_steps:], forecast)

print(f'MSE: {mse}')

# Прогнозирование
next_wave = model_fit.forecast(steps=1)[0]

# Визуализация на карте
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
folium.Marker([55.7558, 37.6173], popup=f'Следующая волна миграции: {next_wave}').add_to(m)
m.save("278.html")