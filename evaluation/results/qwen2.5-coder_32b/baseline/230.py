import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Предположим, что у нас есть два файла: 'eth_price.csv' и 'osk_water_level.csv'
# eth_price.csv содержит столбцы: 'date', 'price'
# osk_water_level.csv содержит столбцы: 'date', 'water_level'

# Загрузка данных
eth_data = pd.read_csv('eth_price.csv', parse_dates=['date'])
water_data = pd.read_csv('osk_water_level.csv', parse_dates=['date'])

# Объединение данных по дате
merged_data = pd.merge(eth_data, water_data, on='date')

# Проверка на пропуски и удаление строк с пропусками
merged_data.dropna(inplace=True)

# Нормализация данных
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
merged_data[['price', 'water_level']] = scaler.fit_transform(merged_data[['price', 'water_level']])

# Разделение данных на обучающую и тестовую выборки
X = merged_data['water_level'].values.reshape(-1, 1)
y = merged_data['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Выбор и обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратичная ошибка: {mse}')

# Визуализация результатов на карте (пример координат реки Осек)
m = folium.Map(location=[56.0184, 37.2081], zoom_start=10)

# Добавление маркера с информацией о предсказании
folium.Marker(
    location=[56.0184, 37.2081],
    popup=f'Предсказанное значение ETH: {y_pred.mean()}',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("230.html")