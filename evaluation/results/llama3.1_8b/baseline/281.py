import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Подготовка данных
data = pd.read_csv('weather_data.csv')

# Обработка данных
data['date'] = pd.to_datetime(data['date'])
data['temperature'] = data['temperature'].astype(float)
data['humidity'] = data['humidity'].astype(float)

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание исторических моделей
historical_model_lr = LinearRegression()
historical_model_rf = RandomForestRegressor()

historical_model_lr.fit(train_data[['temperature', 'humidity']], train_data['weather'])
historical_model_rf.fit(train_data[['temperature', 'humidity']], train_data['weather'])

# Создание современных моделей
modern_model_lr = LinearRegression()
modern_model_rf = RandomForestRegressor()

modern_model_lr.fit(test_data[['temperature', 'humidity']], test_data['weather'])
modern_model_rf.fit(test_data[['temperature', 'humidity']], test_data['weather'])

# Сравнение моделей
historical_lr_accuracy = historical_model_lr.score(train_data[['temperature', 'humidity']], train_data['weather'])
historical_rf_accuracy = historical_model_rf.score(train_data[['temperature', 'humidity']], train_data['weather'])
modern_lr_accuracy = modern_model_lr.score(test_data[['temperature', 'humidity']], test_data['weather'])
modern_rf_accuracy = modern_model_rf.score(test_data[['temperature', 'humidity']], test_data['weather'])

# Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=10)
Marker(location=[55.7558, 37.6173], popup='Исторические модели: LR - {:.2f}, RF - {:.2f}'.format(historical_lr_accuracy, historical_rf_accuracy)).add_to(m)
Marker(location=[55.7558, 37.6173], popup='Современные модели: LR - {:.2f}, RF - {:.2f}'.format(modern_lr_accuracy, modern_rf_accuracy)).add_to(m)

m.save("281.html")