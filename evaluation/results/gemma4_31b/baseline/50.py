import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import folium

# =============================================================================
# 1. Симуляция данных (так как реальный датасет Dos River не предоставлен)
# =============================================================================
np.random.seed(42)
dates = pd.date_range(start="2019-01-01", end="2023-12-31", freq='D')
n_days = len(dates)

# Генерируем синтетические данные: осадки, температура и уровень воды
precipitation = np.random.gamma(2, 2, n_days) 
temperature = 10 + 15 * np.sin(2 * np.pi * np.arange(n_days) / 365) + np.random.randn(n_days) * 2
# Уровень воды зависит от осадков (с задержкой) и температуры (весенний паводок)
water_level = 2.0 + 0.5 * precipitation + 0.1 * (temperature > 0).astype(int) * temperature + np.random.randn(n_days) * 0.5

df = pd.DataFrame({'date': dates, 'precipitation': precipitation, 'temp': temperature, 'level': water_level})

# =============================================================================
# 2. Feature Engineering
# =============================================================================
# Создаем лаги для уровня воды (зависимость от предыдущих дней)
for i in [1, 3, 7]:
    df[f'level_lag_{i}'] = df['level'].shift(i)

# Скользящее среднее осадков за неделю
df['precip_roll_7'] = df['precipitation'].rolling(window=7).mean()

df = df.dropna()

# =============================================================================
# 3. Построение модели прогнозирования
# =============================================================================
X = df[['precipitation', 'temp', 'level_lag_1', 'level_lag_3', 'level_lag_7', 'precip_roll_7']]
y = df['level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогноз на завтра (используя последние данные)
last_features = X.tail(1)
prediction = model.predict(last_features)[0]
print(f"Predicted water level for tomorrow: {prediction:.2f} meters")

# =============================================================================
# 4. Геопространственная визуализация (GIS)
# =============================================================================
# Координаты реки Dos River (симуляция русла)
river_coords = [
    [45.50, -93.20], [45.52, -93.22], [45.55, -93.25], 
    [45.58, -93.28], [45.60, -93.30], [45.62, -93.35]
]

# Определяем критический порог
CRITICAL_THRESHOLD = 5.0
risk_color = 'green' if prediction < CRITICAL_THRESHOLD else 'red'
risk_status = 'Low Risk' if prediction < CRITICAL_THRESHOLD else 'High Flood Risk'

# Создание карты
m = folium.Map(location=[45.55, -93.25], zoom_start=11, tiles='OpenStreetMap')

# Рисуем русло реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Dos River").add_to(m)

# Добавляем маркеры мониторинговых станций
stations = [
    {"name": "Station Alpha", "loc": [45.50, -93.20]},
    {"name": "Station Beta", "loc": [45.55, -93.25]},
    {"name": "Station Gamma", "loc": [45.62, -93.35]},
]

for st in stations:
    folium.CircleMarker(
        location=st["loc"],
        radius=8,
        color=risk_color,
        fill=True,
        fill_color=risk_color,
        popup=f"{st['name']} - Prediction: {prediction:.2f}m ({risk_status})"
    ).add_to(m)

# Добавляем информационную панель
folium.Popup(f"Flood Prediction Model\nPredicted Level: {prediction:.2f}m\nStatus: {risk_status}").add_to(m)

# Сохранение карты
m.save("50.html")
print("Map has been saved as 50.html")