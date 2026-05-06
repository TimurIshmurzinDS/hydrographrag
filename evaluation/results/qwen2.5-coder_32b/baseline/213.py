import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV:
# - 'dos_river_data.csv' с показаниями датчиков Дос-Ривера (столбцы: timestamp, sensor_value)
# - 'ethereum_prices.csv' с ценами на Ethereum (столбцы: timestamp, price)

# Загрузка данных
sensor_data = pd.read_csv('dos_river_data.csv', parse_dates=['timestamp'])
eth_price_data = pd.read_csv('ethereum_prices.csv', parse_dates=['timestamp'])

# Шаг 2: Предварительная обработка данных
# Выравнивание временных рядов и объединение данных
sensor_data.set_index('timestamp', inplace=True)
eth_price_data.set_index('timestamp', inplace=True)

# Пример интерполяции пропусков в данных датчиков
sensor_data = sensor_data.resample('D').mean().interpolate()

# Выравнивание временных рядов и объединение данных
merged_data = pd.merge(sensor_data, eth_price_data, on='timestamp', how='inner')

# Шаг 3: Анализ корреляции
correlation_matrix = merged_data.corr()
print("Корреляционная матрица:")
print(correlation_matrix)

# Шаг 4: Построение модели
X = merged_data[['sensor_value']]
y = merged_data['price']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 5: Оценка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Корень из средней квадратичной ошибки (RMSE): {rmse}")

# Шаг 6: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[34.0522, -118.2437], zoom_start=10)  # Пример координат Лос-Анджелеса

# Добавление маркеров для реальных и прогнозируемых цен на Ethereum
for idx, row in merged_data.iterrows():
    folium.Marker(
        location=[34.0522, -118.2437],  # Пример координат Лос-Анджелеса
        popup=f"Дата: {row.name.date()}, Реальная цена: {row['price']}, Прогнозируемая цена: {model.predict(np.array([[row['sensor_value']]]))[0]}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("213.html")