import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# =============================================================================
# 1. СИНТЕЗ ДАННЫХ (Имитация исторических трендов реки Kurty)
# =============================================================================
np.random.seed(42)
days = 730  # 2 года данных
start_date = datetime(2022, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(days)]

# Создаем уровень воды: Базовый уровень + Сезонность (синус) + Тренд + Шум
time_index = np.arange(days)
seasonal_component = 2.0 * np.sin(2 * np.pi * time_index / 365) 
trend_component = 0.001 * time_index
noise = np.random.normal(0, 0.3, days)
water_levels = 5.0 + seasonal_component + trend_component + noise

df = pd.DataFrame({'date': dates, 'level': water_levels})
df['day_of_year'] = df['date'].dt.dayofyear

# =============================================================================
# 2. ИНЖЕНЕРИЯ ПРИЗНАКОВ (Lags)
# =============================================================================
def create_lags(data, lags=[1, 3, 7]):
    df_lagged = data.copy()
    for lag in lags:
        df_lagged[f'lag_{lag}'] = df_lagged['level'].shift(lag)
    return df_lagged.dropna()

df_model = create_lags(df)

# Разделение на признаки (X) и целевую переменную (y)
X = df_model[['day_of_year', 'lag_1', 'lag_3', 'lag_7']]
y = df_model['level']

# Разделение на train/test (последние 30 дней для теста)
split = len(X) - 30
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# =============================================================================
# 3. ОБУЧЕНИЕ МОДЕЛИ
# =============================================================================
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверка точности
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model MAE: {mae:.4f} meters")

# =============================================================================
# 4. ПРОГНОЗ НА БУДУЩИЙ ПЕРИОД (30 дней)
# =============================================================================
future_days = 30
last_date = df['date'].iloc[-1]
future_dates = [last_date + timedelta(days=i) for i in range(1, future_days + 1)]

# Для простоты прогноза используем последние значения и сезонный тренд
current_level = df['level'].iloc[-1]
future_preds = []
temp_lags = list(df['level'].iloc[-7:]) # последние 7 дней для лагов

for i in range(future_days):
    date_val = future_dates[i].timetuple().tm_yday
    # Формируем признаки для прогноза: [день_года, lag1, lag3, lag7]
    feat = np.array([[date_val, temp_lags[-1], temp_lags[-3], temp_lags[-7]]])
    pred = model.predict(feat)[0]
    future_preds.append(pred)
    temp_lags.append(pred) # Добавляем прогноз в лаги для следующего шага

# =============================================================================
# 5. ГЕОПРОСТРАНСТВЕННАЯ ВИЗУАЛИЗАЦИЯ (Folium)
# =============================================================================
# Координаты реки Kurty (примерные координаты региона)
kurty_coords = [43.25, 70.12] 

# Определяем цвет маркера в зависимости от среднего прогноза
avg_future_level = np.mean(future_preds)
if avg_future_level > 6.5:
    status_color = 'red'    # Высокий уровень (Риск)
    status_text = 'High Water Level Warning'
elif avg_future_level > 5.0:
    status_color = 'orange' # Средний уровень
    status_text = 'Moderate Water Level'
else:
    status_color = 'green'  # Норма
    status_text = 'Normal Water Level'

# Создание карты
m = folium.Map(location=kurty_coords, zoom_start=12, tiles='OpenStreetMap')

# Добавление маркера станции мониторинга
folium.Marker(
    location=kurty_coords,
    popup=f"Kurty River Station<br>Predicted Avg Level: {avg_future_level:.2f}m<br>Status: {status_text}",
    icon=folium.Icon(color=status_color, icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("57.html")

print("Success: Prediction model built and map saved as 57.html")

# Опционально: Визуализация тренда (график)
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['level'], label='Historical Data')
plt.plot(future_dates, future_preds, label='Forecast', color='red', linestyle='--')
plt.title("Water Level Prediction for Kurty River")
plt.xlabel("Date")
plt.ylabel("Water Level (m)")
plt.legend()
plt.grid(True)
plt.show()