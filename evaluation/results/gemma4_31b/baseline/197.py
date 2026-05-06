import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, rmse_score # Note: using mean_squared_error for RMSE
from sklearn.metrics import mean_squared_error

# 1. Симуляция исторических данных (так как реальный датасет Aksu River требует доступа к архивам)
np.random.seed(42)
dates = pd.date_range(start="2010-01-01", end="2023-12-31", freq='M')
n_months = len(dates)

# Генерация синтетического стока с выраженной сезонностью (пик весной)
# Формула: Базовый сток + Синусоида (сезонность) + Шум
discharge = 50 + 40 * np.sin(2 * np.pi * dates.month / 12) + np.random.normal(0, 10, n_months)
temp = 10 + 15 * np.sin(2 * np.pi * dates.month / 12) + np.random.normal(0, 2, n_months)
precip = 20 + 10 * np.cos(2 * np.pi * dates.month / 12) + np.random.normal(0, 5, n_months)

df = pd.DataFrame({'date': dates, 'discharge': discharge, 'temp': temp, 'precip': precip})

# 2. Подготовка признаков для моделирования
def prepare_features(data):
    df_feat = data.copy()
    # Создаем лаги (предыдущие значения)
    df_feat['lag_1'] = df_feat['discharge'].shift(1)
    df_feat['lag_2'] = df_feat['discharge'].shift(2)
    df_feat['month'] = df_feat['date'].dt.month
    # Целевая переменная - сток следующего месяца (прогноз на сезон)
    df_feat['target'] = df_feat['discharge'].shift(-1)
    return df_feat.dropna()

df_model = prepare_features(df)

X = df_model[['temp', 'precip', 'lag_1', 'lag_2', 'month']]
y = df_model['target']

# Разделение на обучающую и тестовую выборки (по времени)
split = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# 3. Обучение модели Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогноз на следующий сезон
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"Model Performance:\nMAE: {mae:.2f}\nRMSE: {rmse:.2f}")

# Прогноз пика на следующий период (симуляция данных для следующего сезона)
next_season_features = np.array([[12.5, 25.0, df_model['discharge'].iloc[-1], df_model['discharge'].iloc[-2], 5]])
predicted_peak = model.predict(next_season_features)[0]
print(f"Predicted Peak Discharge for next season: {predicted_peak:.2f} m3/s")

# 4. Геопространственная визуализация (Folium)
# Координаты реки Aksu (примерные координаты региона Центральной Азии)
river_coords = [
    [43.1, 81.2], [43.2, 81.5], [43.4, 81.8], [43.6, 82.1], [43.8, 82.5]
]

m = folium.Map(location=[43.4, 81.8], zoom_start=8, tiles='OpenStreetMap')

# Рисуем русло реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Aksu River").add_to(m)

# Определяем точки мониторинга и уровень риска на основе прогноза
stations = [
    {"name": "Upper Aksu", "loc": [43.1, 81.2], "risk": "Low"},
    {"name": "Middle Aksu", "loc": [43.4, 81.8], "risk": "Medium"},
    {"name": "Lower Aksu", "loc": [43.8, 82.5], "risk": "High" if predicted_peak > 70 else "Low"},
]

colors = {"Low": "green", "Medium": "orange", "High": "red"}

for st in stations:
    folium.CircleMarker(
        location=st["loc"],
        radius=8,
        color=colors[st["risk"]],
        fill=True,
        fill_color=colors[st["risk"]],
        popup=f"Station: {st['name']}<br>Risk Level: {st['risk']}<br>Pred. Peak: {predicted_peak:.2f} m3/s"
    ).add_to(m)

# Сохранение карты
m.save("197.html")
print("Map has been saved as 197.html")