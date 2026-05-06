import pandas as pd
import numpy as np
import folium
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import datetime

# 1. Генерация синтетических данных
# Создаем временной интервал за последние 100 дней
np.random.seed(42)
dates = pd.date_range(end=datetime.datetime.now(), periods=100)

# Имитируем сток реки Осек (м3/с) - сезонные колебания + шум
river_flow = 50 + 20 * np.sin(np.linspace(0, 3.14, 100)) + np.random.normal(0, 5, 100)

# Имитируем курс Ethereum (USD) - случайное блуждание
eth_price = 2500 + np.cumsum(np.random.normal(0, 50, 100))

df = pd.DataFrame({
    'date': dates,
    'river_flow': river_flow,
    'eth_price': eth_price
})

# 2. Подготовка данных для моделирования
X = df[['river_flow']].values
y = df['eth_price'].values

# Масштабирование признаков
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# 3. Построение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
y_test_actual = scaler_y.inverse_transform(y_test.reshape(-1, 1))

# Метрики
mse = mean_squared_error(y_test_actual, y_pred)
r2 = r2_score(y_test_actual, y_pred)

print(f"Model Performance:\n MSE: {mse:.2f}\n R2 Score: {r2:.4f}")
print(f"Prediction for next flow value (e.g., 60 m3/s): {model.predict([[scaler_X.transform([[60]])[0][0]]])[0]}")

# 4. Геопространственная визуализация (GIS)
# Предположим координаты реки Осек (условные координаты для демонстрации)
# В реальности здесь должны быть точные координаты гидропоста
osek_river_coords = [45.1234, 75.5678] 

m = folium.Map(location=osek_river_coords, zoom_start=10, tiles='OpenStreetMap')

# Добавление маркера реки
folium.Marker(
    location=osek_river_coords,
    popup=f"Река Осек\nСредний сток: {df['river_flow'].mean():.2f} м3/с",
    tooltip="Объект мониторинга: Река Осек",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление текстового пояснения на карту
folium.Popup(f"Модель предсказания ETH на основе стока реки. R2: {r2:.4f}").add_to(m)

# Сохранение карты строго по условию
m.save("230.html")

print("\nMap has been saved as 230.html")