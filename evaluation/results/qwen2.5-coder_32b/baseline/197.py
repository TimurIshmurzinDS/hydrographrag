import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о стоках воды
data = pd.read_csv('aksu_river_flow_data.csv', parse_dates=['date'], index_col='date')

# Проверяем первые строки данных
print(data.head())

# Шаг 2: Анализ временных рядов
plt.figure(figsize=(14,7))
plt.plot(data['flow'])
plt.title('Исторические данные о стоках воды реки Aksu River')
plt.xlabel('Дата')
plt.ylabel('Сток воды (куб. м/с)')
plt.show()

# Шаг 3: Выбор модели прогнозирования
# Используем модель SARIMA для учета сезонности
model = SARIMAX(data['flow'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))

# Шаг 4: Обучение модели
model_fit = model.fit(disp=False)

# Выводим результаты обучения
print(model_fit.summary())

# Шаг 5: Валидация модели
# Разделяем данные на обучающую и тестовую выборки
train_size = int(len(data) * 0.8)
train, test = data['flow'][:train_size], data['flow'][train_size:]

# Прогнозирование на тестовой выборке
predictions = model_fit.forecast(steps=len(test))

# Визуализация результатов прогнозирования
plt.figure(figsize=(14,7))
plt.plot(train.index, train.values, label='Обучающая выборка')
plt.plot(test.index, test.values, label='Тестовая выборка')
plt.plot(test.index, predictions, label='Прогноз', color='red')
plt.title('Прогнозирование стока воды реки Aksu River')
plt.xlabel('Дата')
plt.ylabel('Сток воды (куб. м/с)')
plt.legend()
plt.show()

# Шаг 6: Прогнозирование на следующий сезон
forecast = model_fit.forecast(steps=12)  # Предположим, что сезон длится 12 месяцев

# Визуализация прогноза на следующий сезон
plt.figure(figsize=(14,7))
plt.plot(data.index, data['flow'], label='Исторические данные')
plt.plot(pd.date_range(start=data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M'), forecast, label='Прогноз на следующий сезон', color='green')
plt.title('Прогноз пиковых значений уровня воды реки Aksu River на следующий сезон')
plt.xlabel('Дата')
plt.ylabel('Сток воды (куб. м/с)')
plt.legend()
plt.show()

# Шаг 7: Визуализация результатов на карте
# Предположим, что у нас есть координаты реки Aksu River
m = folium.Map(location=[42.8609, 75.1312], zoom_start=10)  # Координаты примерные

# Добавляем маркер на карту
folium.Marker(
    location=[42.8609, 75.1312],
    popup='Прогноз пиковых значений уровня воды реки Aksu River',
    icon=folium.Icon(color='red')
).add_to(m)

# Сохраняем карту
m.save("197.html")