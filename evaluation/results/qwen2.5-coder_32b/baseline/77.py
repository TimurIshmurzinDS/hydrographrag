import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import folium

# Предполагаем, что у нас есть данные о дисхаргее для двух рек в формате CSV.
# Данные должны содержать столбцы: 'date', 'discharge_Baskan', 'discharge_Prokhodnaya'

# Загрузка данных
data = pd.read_csv('discharge_data.csv', parse_dates=['date'], index_col='date')

# Обработка данных (удаление пропусков)
data.dropna(inplace=True)

# Анализ сезонности для Баскан Реки
result_Baskan = seasonal_decompose(data['discharge_Baskan'], model='additive')
result_Baskan.plot()
plt.title('Сезонность дисхаргера Баскан Реки')
plt.show()

# Анализ сезонности для Прокходной Реки
result_Prokhodnaya = seasonal_decompose(data['discharge_Prokhodnaya'], model='additive')
result_Prokhodnaya.plot()
plt.title('Сезонность дисхаргера Прокходной Реки')
plt.show()

# Сравнение сезонных уровней расхода
seasonal_Baskan = result_Baskan.seasonal
seasonal_Prokhodnaya = result_Prokhodnaya.seasonal

plt.figure(figsize=(14, 7))
plt.plot(seasonal_Baskan.index, seasonal_Baskan.values, label='Баскан Река')
plt.plot(seasonal_Prokhodnaya.index, seasonal_Prokhodnaya.values, label='Прокходная Река')
plt.title('Сравнение сезонных уровней расхода')
plt.xlabel('Дата')
plt.ylabel('Уровень дисхаргера')
plt.legend()
plt.show()

# Прогнозирование весеннего половодья
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Прогноз для Баскан Реки
model_Baskan = ExponentialSmoothing(data['discharge_Baskan'], trend='add', seasonal='add', seasonal_periods=12)
fit_Baskan = model_Baskan.fit()
forecast_Baskan = fit_Baskan.forecast(3)  # Прогноз на три месяца вперед

# Прогноз для Прокходной Реки
model_Prokhodnaya = ExponentialSmoothing(data['discharge_Prokhodnaya'], trend='add', seasonal='add', seasonal_periods=12)
fit_Prokhodnaya = model_Prokhodnaya.fit()
forecast_Prokhodnaya = fit_Prokhodnaya.forecast(3)  # Прогноз на три месяца вперед

# Визуализация прогноза
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['discharge_Baskan'], label='Баскан Река (исторические данные)')
plt.plot(forecast_Baskan.index, forecast_Baskan.values, label='Прогноз Баскан Реки', linestyle='--')
plt.plot(data.index, data['discharge_Prokhodnaya'], label='Прокходная Река (исторические данные)')
plt.plot(forecast_Prokhodnaya.index, forecast_Prokhodnaya.values, label='Прогноз Прокходной Реки', linestyle='--')
plt.title('Прогноз дисхаргера рек в весенний период')
plt.xlabel('Дата')
plt.ylabel('Уровень дисхаргера')
plt.legend()
plt.show()

# Визуализация на карте с использованием folium
m = folium.Map(location=[56.0, 143.0], zoom_start=7)

# Координаты рек (примерные)
baskan_coords = [55.9822, 142.9844]
prokhodnaya_coords = [56.0333, 143.05]

folium.Marker(baskan_coords, popup='Баскан Река').add_to(m)
folium.Marker(prokhodnaya_coords, popup='Прокходная Река').add_to(m)

# Добавление кругов для визуализации уровня дисхаргера
folium.CircleMarker(
    location=baskan_coords,
    radius=forecast_Baskan.iloc[-1] / 50,  # Примерный масштабирование радиуса
    color='blue',
    fill=True,
    fill_color='blue'
).add_to(m)

folium.CircleMarker(
    location=prokhodnaya_coords,
    radius=forecast_Prokhodnaya.iloc[-1] / 50,  # Примерный масштабирование радиуса
    color='red',
    fill=True,
    fill_color='red'
).add_to(m)

m.save("77.html")