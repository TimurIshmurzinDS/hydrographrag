import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Пример данных: показания датчиков Dos River и цены на Ethereum
data = {
    'Dos_River_Sensor': [10, 20, 30, 40, 50],
    'Ethereum_Price': [2000, 2100, 2200, 2300, 2400]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df['Dos_River_Sensor'].values.reshape(-1, 1), df['Ethereum_Price'], test_size=0.2, random_state=42)

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f"Средняя ошибка квадратичная: {mse}")

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[37.421998, -122.084], zoom_start=13)

for idx, row in df.iterrows():
    folium.Marker([37.421998, -122.084], popup=f"Датчик Dos River: {row['Dos_River_Sensor']}, Цена Ethereum: {row['Ethereum_Price']}").add_to(m)

m.save("213.html")