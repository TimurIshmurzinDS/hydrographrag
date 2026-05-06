import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть CSV файл с историческими данными о водном уровне реки Dos River
# Файл должен содержать столбцы 'date' и 'water_level'
data = pd.read_csv('dos_river_water_level.csv', parse_dates=['date'], index_col='date')

# Проверка первых строк данных
print(data.head())

# Анализ временного ряда
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['water_level'])
plt.title('Исторический уровень воды в реке Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.show()

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(data) * 0.8)
train, test = data['water_level'][:train_size], data['water_level'][train_size:]

# Обучение модели ARIMA
model = ARIMA(train, order=(5,1,0))  # Параметры (p,d,q) могут быть выбраны по результатам анализа ACF и PACF
model_fit = model.fit()

# Предсказание на тестовой выборке
predictions = model_fit.forecast(steps=len(test))
plt.figure(figsize=(12, 6))
plt.plot(data.index[train_size:], test, label='Тестовые данные')
plt.plot(data.index[train_size:], predictions, color='red', label='Предсказания')
plt.title('Сравнение тестовых данных и предсказаний')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()

# Предсказание на будущий период (например, 30 дней)
future_predictions = model_fit.forecast(steps=30)

# Создание датафрейма с предсказанными значениями
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=30)
future_df = pd.DataFrame({'date': future_dates, 'predicted_water_level': future_predictions})
future_df.set_index('date', inplace=True)

# Визуализация предсказанных значений на карте
# Предположим, что у нас есть координаты реки Dos River (широта и долгота)
river_lat = 32.4569
river_lon = -108.7817

m = folium.Map(location=[river_lat, river_lon], zoom_start=10)

# Добавление маркера с текущим уровнем воды
folium.Marker(
    location=[river_lat, river_lon],
    popup=f"Текущий уровень воды: {data['water_level'].iloc[-1]}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Добавление линии предсказанных значений
coordinates = [(river_lat + 0.001 * i, river_lon) for i in range(len(future_df))]
folium.PolyLine(
    locations=coordinates,
    color="red",
    weight=2.5,
    opacity=1
).add_to(m)

# Сохранение карты в HTML файл
m.save("221.html")