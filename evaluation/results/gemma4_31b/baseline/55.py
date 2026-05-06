import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import folium

# ==========================================
# 1. Симуляция исторических данных
# ==========================================
# В реальном сценарии здесь будет: df = pd.read_csv("batareyka_levels.csv")
np.random.seed(42)
dates = pd.date_range(start="2021-01-01", end="2023-12-31", freq='D')
n_days = len(dates)

# Создаем синтетический уровень воды: Тренд + Сезонность (синус) + Шум
trend = np.linspace(1.0, 1.2, n_days)  # Медленный подъем уровня за 3 года
seasonality = 0.5 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
noise = np.random.normal(0, 0.1, n_days)
water_levels = 2.0 + trend + seasonality + noise

df = pd.DataFrame({'date': dates, 'level': water_levels})

# ==========================================
# 2. Подготовка признаков для моделирования
# ==========================================
def create_features(data):
    df_feat = data.copy()
    df_feat['day_of_year'] = df_feat['date'].dt.dayofyear
    # Используем sin/cos для кодирования цикличности года
    df_feat['sin_day'] = np.sin(2 * np.pi * df_feat['day_of_year'] / 365.25)
    df_feat['cos_day'] = np.cos(2 * np.pi * df_feat['day_of_year'] / 365.25)
    # Линейный тренд (порядковый номер дня)
    df_feat['trend'] = (df_feat['date'] - df_feat['date'].min()).dt.days
    return df_feat

df_model = create_features(df)
X = df_model[['sin_day', 'cos_day', 'trend']]
y = df_model['level']

# Обучение модели
model = LinearRegression()
model.fit(X, y)

# ==========================================
# 3. Прогноз на предстоящий год (2024)
# ==========================================
future_dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq='D')
future_df = pd.DataFrame({'date': future_dates})
future_feat = create_features(future_df)

X_future = future_feat[['sin_day', 'cos_day', 'trend']]
predictions = model.predict(X_future)
future_df['predicted_level'] = predictions

# ==========================================
# 4. Визуализация графиков
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['level'], label='Historical Data', color='blue')
plt.plot(future_df['date'], future_df['predicted_level'], label='Forecast 2024', color='red', linestyle='--')
plt.title('Water Level Prediction for Batareyka River')
plt.xlabel('Date')
plt.ylabel('Water Level (m)')
plt.legend()
plt.grid(True)
plt.savefig("forecast_plot.png")
plt.show()

# ==========================================
# 5. Геопространственная визуализация (Folium)
# ==========================================
# Координаты реки Batareyka (примерные координаты для демонстрации)
# В реальности используются точные координаты гидропоста
river_coords = [53.45, 29.50] 

m = folium.Map(location=river_coords, zoom_start=12, tiles='OpenStreetMap')

# Добавляем маркер станции мониторинга
folium.Marker(
    location=river_coords,
    popup="Batareyka River Monitoring Station",
    tooltip="Station Alpha",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавляем текстовое описание прогноза в всплывающее окно или отдельный элемент
folium.Popup(f"Predicted Avg Level 2024: {future_df['predicted_level'].mean():.2f}m").add_to(m)

# Сохранение карты строго по условию
m.save("55.html")

print("Modeling complete. Forecast plot saved as 'forecast_plot.png' and map saved as '55.html'.")