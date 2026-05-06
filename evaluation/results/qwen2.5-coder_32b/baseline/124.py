import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о уровнях воды реки Dos River
data = pd.read_csv('dos_river_water_levels.csv', parse_dates=['date'], index_col='date')

# Проверяем данные
print(data.head())

# Шаг 2: Анализ временных рядов
plt.figure(figsize=(14,7))
plt.plot(data.index, data['water_level'])
plt.title('Уровень воды реки Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.show()

# Шаг 3: Выбор модели прогнозирования
# Используем SARIMAX для учета сезонности
model = SARIMAX(data['water_level'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit()

# Шаг 4: Обучение модели
print(results.summary())

# Шаг 5: Валидация модели
data['forecast'] = results.predict(start=0, end=len(data)-1)
plt.figure(figsize=(14,7))
plt.plot(data.index, data['water_level'], label='Фактические данные')
plt.plot(data.index, data['forecast'], label='Прогноз', color='red')
plt.title('Сравнение фактических данных и прогноза для реки Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Шаг 6: Прогнозирование уровня воды
forecast_steps = 365 * 3  # Прогноз на 3 года вперед
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)

# Прогноз для 2025 года
forecast_2025 = forecast_series['2025']
plt.figure(figsize=(14,7))
plt.plot(data.index, data['water_level'], label='Фактические данные')
plt.plot(forecast_index, forecast.predicted_mean, label='Прогноз', color='red')
plt.title('Прогноз уровня воды реки Lepsy River на 2025 год')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Шаг 7: Визуализация результатов
# Предположим, что у нас есть координаты реки Lepsy River
m = folium.Map(location=[51.684023, 39.191481], zoom_start=10)

# Добавляем точки прогноза на карту
for date, level in forecast_2025.items():
    folium.CircleMarker(
        location=[51.684023, 39.191481],
        radius=level * 10,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Дата: {date.strftime("%Y-%m-%d")}\nУровень воды: {level:.2f} м'
    ).add_to(m)

# Сохраняем карту
m.save("124.html")