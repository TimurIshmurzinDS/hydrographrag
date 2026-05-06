import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о уровне воды в реке Dos River
data = pd.read_csv('dos_river_water_level.csv', parse_dates=['date'], index_col='date')

# Проверяем первые строки данных
print(data.head())

# Шаг 2: Предварительная обработка данных
# Удаляем пропуски и проверяем наличие аномалий
data = data.dropna()

# Визуализация временного ряда для анализа тренда и сезонности
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['water_level'], label='Уровень воды')
plt.title('Исторический уровень воды в реке Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Шаг 3: Выбор модели
# Используем модель ARIMA для прогнозирования временного ряда

# Разделяем данные на обучающую и тестовую выборки
train_size = int(len(data) * 0.8)
train, test = data['water_level'][:train_size], data['water_level'][train_size:]

# Обучаем модель ARIMA
model = ARIMA(train, order=(5,1,0))
model_fit = model.fit()

# Шаг 4: Валидация модели
# Прогнозируем значения на тестовой выборке
forecast = model_fit.forecast(steps=len(test))

# Сравниваем прогноз с фактическими данными
plt.figure(figsize=(14, 7))
plt.plot(test.index, test.values, label='Фактические данные')
plt.plot(test.index, forecast, label='Прогноз', color='red')
plt.title('Сравнение фактических данных и прогноза уровня воды')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.show()

# Шаг 5: Прогнозирование уровня воды
# Прогнозируем уровень воды на следующие 30 дней
future_forecast = model_fit.forecast(steps=30)

# Создаем DataFrame для прогнозируемых значений
forecast_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=30)
forecast_df = pd.DataFrame({'date': forecast_dates, 'predicted_water_level': future_forecast})
forecast_df.set_index('date', inplace=True)

# Шаг 6: Визуализация результатов
# Предположим, что у нас есть координаты реки Dos River для визуализации на карте
river_coordinates = (32.5047, -114.985)  # Примерные координаты

# Создаем карту с помощью folium
m = folium.Map(location=river_coordinates, zoom_start=10)

# Добавляем маркеры для исторических данных и прогнозируемых значений
for date, level in data.iterrows():
    folium.Marker(
        location=(river_coordinates[0], river_coordinates[1]),
        popup=f"Дата: {date.strftime('%Y-%m-%d')}, Уровень воды: {level['water_level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

for date, level in forecast_df.iterrows():
    folium.Marker(
        location=(river_coordinates[0], river_coordinates[1]),
        popup=f"Дата: {date.strftime('%Y-%m-%d')}, Прогнозируемый уровень воды: {level['predicted_water_level']} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохраняем карту в файл
m.save("50.html")