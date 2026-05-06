import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных
data = pd.read_csv('bayankol_data.csv')  # Предположим, что данные находятся в файле bayankol_data.csv

# Проверка первых строк данных
print(data.head())

# Подготовка данных
# Предположим, что мы хотим использовать уровень воды и температуру для предсказания курса биткоина
features = data[['water_level', 'temperature']]
target = data['bitcoin_price']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Построение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for idx, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Water Level: {row['water_level']}, Temperature: {row['temperature']}, Bitcoin Price: {row['bitcoin_price']}").add_to(m)

m.save("271.html")