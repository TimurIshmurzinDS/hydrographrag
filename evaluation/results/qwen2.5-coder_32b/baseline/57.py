import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о уровне воды
data = pd.read_csv('kurty_river_water_level.csv', parse_dates=['date'], index_col='date')

# Проверяем первые строки данных
print(data.head())

# Шаг 2: Предварительный анализ данных
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['water_level'])
plt.title('Исторический уровень воды в реке Kurty River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.show()

# Шаг 3: Выбор модели
# Используем модель ARIMA для временного ряда
model = ARIMA(data['water_level'], order=(5,1,0))

# Шаг 4: Обучение модели
model_fit = model.fit()

# Шаг 5: Валидация модели
forecast = model_fit.forecast(steps=365)  # Прогноз на год вперед

# Шаг 6: Прогнозирование
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['water_level'], label='Исторические данные')
plt.plot(pd.date_range(start=data.index[-1], periods=365, freq='D'), forecast, color='red', label='Прогноз')
plt.title('Прогноз уровня воды в реке Kurty River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Шаг 7: Визуализация результатов на карте
# Предположим, что у нас есть координаты месторасположения измерений уровня воды
latitude = 52.381046  # Примерные координаты реки Kurty River
longitude = 49.767858

m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавляем маркер с текущим уровнем воды
folium.Marker(
    location=[latitude, longitude],
    popup=f"Текущий уровень воды: {data['water_level'].iloc[-1]} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохраняем карту в HTML файл
m.save("57.html")