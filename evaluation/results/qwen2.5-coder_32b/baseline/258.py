import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два CSV файла: 'water_level_emel.csv' и 'bitcoin_price.csv'
# water_level_emel.csv содержит столбцы: date, water_level
# bitcoin_price.csv содержит столбцы: date, price

# Загрузка данных
water_level_data = pd.read_csv('water_level_emel.csv', parse_dates=['date'])
bitcoin_price_data = pd.read_csv('bitcoin_price.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Выравнивание временных рядов по датам и объединение их в один DataFrame
merged_data = pd.merge(water_level_data, bitcoin_price_data, on='date')

# Проверка на пропуски
print(merged_data.isnull().sum())

# Удаление строк с пропусками
merged_data.dropna(inplace=True)

# Шаг 3: Анализ корреляции
correlation, _ = pearsonr(merged_data['water_level'], merged_data['price'])
print(f'Корреляция между уровнем воды и курсом биткоина: {correlation}')

# Построение графика для визуального анализа
plt.figure(figsize=(14, 7))
plt.plot(merged_data['date'], merged_data['water_level'], label='Уровень воды')
plt.plot(merged_data['date'], merged_data['price'], label='Курс биткоина', color='orange')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title('Уровень воды и курс биткоина по времени')
plt.legend()
plt.show()

# Шаг 4: Моделирование
# Для простоты используем линейную регрессию для моделирования зависимости курса биткоина от уровня воды
from sklearn.linear_model import LinearRegression

X = merged_data[['water_level']]
y = merged_data['price']

model = LinearRegression()
model.fit(X, y)

# Предсказание курса биткоина на основе уровня воды
merged_data['predicted_price'] = model.predict(X)

# Шаг 5: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[51.48, -2.6], zoom_start=10)  # Координаты Эмеля

# Добавление маркера для местоположения реки Эмел
folium.Marker(
    location=[51.48, -2.6],
    popup='Река Эмел',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в HTML файл
m.save("258.html")

# Вывод результатов моделирования
plt.figure(figsize=(14, 7))
plt.plot(merged_data['date'], merged_data['price'], label='Фактический курс биткоина', color='orange')
plt.plot(merged_data['date'], merged_data['predicted_price'], label='Предсказанный курс биткоина', linestyle='--')
plt.xlabel('Дата')
plt.ylabel('Курс биткоина')
plt.title('Сравнение фактического и предсказанного курса биткоина')
plt.legend()
plt.show()