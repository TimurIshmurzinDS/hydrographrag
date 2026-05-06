import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV:
# - 'batareyka_water_level.csv' с колонками ['date', 'water_level']
# - 'bitcoin_price.csv' с колонками ['date', 'price']

# Загрузка данных
water_level_data = pd.read_csv('batareyka_water_level.csv', parse_dates=['date'])
bitcoin_price_data = pd.read_csv('bitcoin_price.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Выравнивание временных рядов и объединение данных
merged_data = pd.merge(water_level_data, bitcoin_price_data, on='date')
merged_data.dropna(inplace=True)

# Шаг 3: Анализ корреляции
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['price'], merged_data['water_level'])
plt.xlabel('Цена биткоина')
plt.ylabel('Уровень воды в реке Batareyka')
plt.title('Корреляция между ценой биткоина и уровнем воды')
plt.show()

# Шаг 4: Построение модели
# Используем ARIMA для временного ряда уровня воды с учетом курса биткоина как внешней переменной

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(merged_data) * 0.8)
train, test = merged_data[:train_size], merged_data[train_size:]

# Обучение модели ARIMA
model = ARIMA(train['water_level'], exog=train['price'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование на тестовой выборке
forecast = model_fit.forecast(steps=len(test), exog=test['price'])

# Шаг 5: Валидация модели
plt.figure(figsize=(10, 6))
plt.plot(test.index, test['water_level'], label='Фактический уровень воды')
plt.plot(test.index, forecast, color='red', label='Прогнозируемый уровень воды')
plt.xlabel('Дата')
plt.ylabel('Уровень воды в реке Batareyka')
plt.title('Сравнение фактического и прогнозируемого уровней воды')
plt.legend()
plt.show()

# Шаг 6: Прогнозирование
# Предположим, что у нас есть будущие данные о ценах биткоина
future_bitcoin_prices = pd.read_csv('future_bitcoin_price.csv', parse_dates=['date'])
forecast_future = model_fit.forecast(steps=len(future_bitcoin_prices), exog=future_bitcoin_prices['price'])

# Шаг 7: Визуализация результатов на карте
# Предположим, что у нас есть координаты реки Batareyka
batareyka_coords = (53.208946, 45.128308)

m = folium.Map(location=batareyka_coords, zoom_start=12)
folium.Marker(batareyka_coords, popup='Batareyka River').add_to(m)

# Добавление прогнозируемого уровня воды на карту
for i in range(len(forecast_future)):
    folium.CircleMarker(
        location=batareyka_coords,
        radius=forecast_future[i] / 10,  # Простое масштабирование радиуса для визуализации
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Прогнозируемый уровень воды: {forecast_future[i]}'
    ).add_to(m)

m.save("212.html")