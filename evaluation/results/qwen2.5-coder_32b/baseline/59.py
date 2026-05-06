import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных (пример синтетических данных)
np.random.seed(0)
dates = pd.date_range(start='2010-01-01', end='2023-12-31')
water_flow = np.sin(np.linspace(0, 10 * np.pi, len(dates))) * 100 + np.random.normal(0, 5, len(dates))
data = pd.DataFrame({'Date': dates, 'WaterFlow': water_flow})
data.set_index('Date', inplace=True)

# Шаг 2: Обработка данных
data.dropna(inplace=True)

# Шаг 3: Анализ временных рядов (простой график)
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['WaterFlow'], label='Расход воды')
plt.title('Исторический расход воды в реке Шилик')
plt.xlabel('Дата')
plt.ylabel('Расход воды, м³/с')
plt.legend()
plt.show()

# Шаг 4: Выбор модели (ARIMA)
model = ARIMA(data['WaterFlow'], order=(5,1,0))
model_fit = model.fit()

# Шаг 5: Обучение модели
print(model_fit.summary())

# Шаг 6: Валидация модели (простая визуализация остатков)
residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2, figsize=(14,7))
residuals.plot(title="Остатки", ax=ax[0])
residuals.plot(kind='kde', title='Распределение остатков', ax=ax[1])
plt.show()

# Шаг 7: Предсказание
forecast = model_fit.forecast(steps=365*10)  # на следующее десятилетие
future_dates = pd.date_range(start='2024-01-01', periods=365*10)
forecast_df = pd.DataFrame({'Date': future_dates, 'ForecastedFlow': forecast})
forecast_df.set_index('Date', inplace=True)

# Найдем максимальное значение предсказанного расхода воды
max_forecast = forecast_df['ForecastedFlow'].max()
print(f"Максимальный прогнозируемый расход воды на следующее десятилетие: {max_forecast} м³/с")

# Шаг 8: Визуализация результатов (folium)
m = folium.Map(location=[51.672044, 39.184303], zoom_start=10)  # примерные координаты реки Шилик

# Добавим маркер с максимальным значением предсказанного расхода воды
max_date = forecast_df['ForecastedFlow'].idxmax()
folium.Marker(
    location=[51.672044, 39.184303],  # примерные координаты реки Шилик
    popup=f"Максимальный прогнозируемый расход воды: {max_forecast} м³/с\nДата: {max_date}",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в файл
m.save("59.html")