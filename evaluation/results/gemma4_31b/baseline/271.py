import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import folium

# 1. Генерация синтетических данных
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", end="2023-12-31", freq='D')
n = len(dates)

# Имитация уровня воды в реке Баянкол (сезонность + шум)
# Синусоида имитирует весенние паводки и летние межени
river_level = 10 + 5 * np.sin(2 * np.pi * np.arange(n) / 365) + np.random.normal(0, 1, n)

# Имитация курса Биткоина (случайное блуждание с трендом)
btc_price = 30000 + np.cumsum(np.random.normal(10, 500, n))

df = pd.DataFrame({'Date': dates, 'River_Level': river_level, 'BTC_Price': btc_price})
df.set_index('Date', inplace=True)

# 2. Подготовка данных для моделирования
# Создаем лаг (сдвиг) в 7 дней: уровень реки сегодня влияет на BTC через неделю
df['River_Lag7'] = df['River_Level'].shift(7)
df.dropna(inplace=True)

X = df[['River_Lag7']]
y = df['BTC_Price']

# Масштабирование
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# 3. Обучение модели
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание
y_pred = model.predict(X_test)

# Метрики
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Model R2 Score: {r2:.4f}")
print(f"Model MSE: {mse:.4f}")
print("Conclusion: If R2 is very low, there is no predictive power.")

# 4. Визуализация результатов
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(df.index, df['River_Level'], color='blue', label='River Level')
plt.title("Bayankol River Level")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df.index, df['BTC_Price'], color='orange', label='BTC Price')
plt.title("Bitcoin Price")
plt.legend()
plt.tight_layout()
plt.show()

# 5. GIS Визуализация (Локация реки Баянкол, Казахстан)
# Приблизительные координаты бассейна реки Баянкол
coords = [46.5, 66.0] 

m = folium.Map(location=coords, zoom_start=6, tiles='OpenStreetMap')

# Добавление маркера реки
folium.Marker(
    location=coords,
    popup="Bayankol River Area",
    tooltip="Data Source for BTC Prediction",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление круга влияния (условная зона мониторинга)
folium.Circle(
    location=coords,
    radius=50000,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.2
).add_to(m)

m.save("271.html")
print("Map has been saved as 271.html")