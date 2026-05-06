import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Сбор данных (пример: использование библиотеки yfinance для получения исторических данных)
import yfinance as yf

# Загрузка данных
tickers = ['BTC-USD', 'ETH-USD', 'LTC-USD']
data = yf.download(tickers, period='1y')

# Предварительная обработка данных
data['Return'] = data['Close'].pct_change().dropna()
data['Volatility'] = data['Return'].rolling(window=20).std()

# Удаление пропущенных значений
data.dropna(inplace=True)

# Разделение данных на признаки и целевую переменную
X = data[['Volatility']]
y = data['Return']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[data['Close'].mean(), data['Volatility'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['Close'], row['Volatility']], popup=f"Date: {row.name.date()}, Volatility: {row['Volatility']:.2f}, Return: {row['Return']:.2%}").add_to(m)

m.save("282.html")