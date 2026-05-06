import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Загрузка данных (предположим, что данные находятся в CSV файле с колонками 'date' и 'discharge')
data = pd.read_csv('shilik_river_discharge.csv', parse_dates=['date'], index_col='date')

# Анализ временного ряда
plt.figure(figsize=(12, 6))
plt.plot(data['discharge'])
plt.title('Исторический расход воды в реке Shilik River')
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.show()

# Проверка стационарности
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['discharge'])
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

# Если временной ряд нестационарен, применяем дифференцирование
if result[1] > 0.05:
    data_diff = data['discharge'].diff().dropna()
else:
    data_diff = data['discharge']

# Обучение модели ARIMA
model = ARIMA(data['discharge'], order=(5, 1, 0))  # Параметры (p, d, q) могут быть подобраны по AIC/BIC
model_fit = model.fit()

# Прогнозирование на следующий месяц
forecast = model_fit.forecast(steps=30)  # Предполагаем, что месяц состоит из 30 дней

# Визуализация результатов
plt.figure(figsize=(12, 6))
plt.plot(data['discharge'], label='Исторические данные')
plt.plot(pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=30, freq='D'), forecast, label='Прогноз', color='red')
plt.title('Прогноз расхода воды в реке Shilik River на следующий месяц')
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.legend()
plt.show()

# Визуализация на карте с использованием folium
# Предположим, что у нас есть координаты реки Shilik River
m = folium.Map(location=[51.8329, 47.6011], zoom_start=10)  # Координаты примерные

folium.Marker(
    location=[51.8329, 47.6011],
    popup='Shilik River',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты
m.save("47.html")