import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть данные в CSV файле с колонками 'date' и 'water_level'
data = pd.read_csv('batareyka_river_water_levels.csv', parse_dates=['date'], index_col='date')

# Проверка данных на пропуски
print(data.isnull().sum())

# Визуализация временного ряда
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['water_level'])
plt.title('Уровень воды в реке Batareyka River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.show()

# Разделение данных на тренировочную и тестовую выборки
train_data = data[:'2022-12-31']
test_data = data['2023-01-01':]

# Определение параметров модели ARIMA с помощью AIC
from statsmodels.tsa.stattools import adfuller

def adf_test(series):
    result = adfuller(series)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])

adf_test(train_data['water_level'])

# Разность первого порядка для стабилизации среднего
train_diff = train_data['water_level'].diff().dropna()
adf_test(train_diff)

from pmdarima import auto_arima

model = auto_arima(train_data['water_level'], seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True)
print(model.summary())

# Обучение модели ARIMA
model_fit = model.fit(train_data['water_level'])

# Предсказание уровня воды на следующий год
forecast = model_fit.predict(n_periods=len(test_data) + 365)
forecast_index = pd.date_range(start=test_data.index[-1] + pd.Timedelta(days=1), periods=len(forecast))
forecast_series = pd.Series(forecast, index=forecast_index)

# Визуализация результатов
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data['water_level'], label='Исторические данные')
plt.plot(test_data.index, test_data['water_level'], label='Тестовые данные', color='orange')
plt.plot(forecast_series.index, forecast_series, label='Прогноз', color='red')
plt.title('Уровень воды в реке Batareyka River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()

# Предположим, что у нас есть координаты месторасположения измерений уровня воды
coordinates = (53.208944, 50.127612)  # Примерные координаты реки Batareyka

# Создание карты с использованием folium
m = folium.Map(location=coordinates, zoom_start=12)

# Добавление маркера на карту
folium.Marker(
    location=coordinates,
    popup='Прогноз уровня воды',
    tooltip='Batareyka River'
).add_to(m)

# Сохранение карты в HTML файл
m.save("55.html")