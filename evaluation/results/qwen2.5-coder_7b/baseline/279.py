import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных
data = pd.read_csv('real_estate_data.csv')

# Проверка первых строк данных
print(data.head())

# Выбор признаков и целевой переменной
X = data[['area', 'num_rooms', 'distance_to_city_center']]
y = data['price']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=13)

for idx, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Price: {row['price']}, Area: {row['area']} sqm, Rooms: {row['num_rooms']}",
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(m)

# Сохранение карты
m.save("279.html")