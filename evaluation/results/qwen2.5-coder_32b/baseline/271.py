import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть два файла CSV:
# - 'bayankol_river_data.csv' с данными о реке (дата, уровень воды)
# - 'bitcoin_price_data.csv' с данными о курсе биткоина (дата, цена)

river_data = pd.read_csv('bayankol_river_data.csv', parse_dates=['date'])
bitcoin_data = pd.read_csv('bitcoin_price_data.csv', parse_dates=['date'])

# Объединим данные по дате
merged_data = pd.merge(river_data, bitcoin_data, on='date')

# Шаг 2: Анализ корреляции
correlation_matrix = merged_data.corr()
print("Корреляционная матрица:")
print(correlation_matrix)

# Построим график для визуального анализа корреляции
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['water_level'], merged_data['price'])
plt.xlabel('Уровень воды реки')
plt.ylabel('Цена биткоина')
plt.title('Корреляция уровня воды и цены биткоина')
plt.show()

# Шаг 3: Построение модели предсказания
X = merged_data[['water_level']]
y = merged_data['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f"Среднеквадратическая ошибка: {mse}")

# Шаг 4: Визуализация результатов
# Для визуализации предположим, что у нас есть координаты местонахождения реки
m = folium.Map(location=[51.2839, 76.9270], zoom_start=10)  # Координаты примерно посередине Баянколового Река

# Добавим маркер на карту
folium.Marker([51.2839, 76.9270], popup='Баянколовый Река').add_to(m)

# Сохранение карты в HTML файл
m.save("271.html")

# Вывод предсказанных значений и фактических для сравнения
comparison_df = pd.DataFrame({'Фактические значения': y_test, 'Предсказанные значения': y_pred})
print(comparison_df.head())