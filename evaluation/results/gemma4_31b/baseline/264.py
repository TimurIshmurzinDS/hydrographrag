import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium
from datetime import datetime, timedelta

# 1. Генерация синтетических данных
np.random.seed(42)
days = 365
dates = pd.date_range(start="2023-01-01", periods=days)

# Моделируем уровень воды: тренд + сезонность (синус) + шум
time_index = np.arange(days)
seasonal_component = 2 * np.sin(2 * np.pi * time_index / 365) 
trend_component = 0.002 * time_index
noise = np.random.normal(0, 0.5, days)
water_levels = 5 + seasonal_component + trend_component + noise

df = pd.DataFrame({'Date': dates, 'WaterLevel': water_levels})

# 2. Прогноз уровня воды на следующие 30 дней
future_days = 30
future_dates = pd.date_range(start=dates[-1] + timedelta(days=1), periods=future_days)
future_index = np.arange(days, days + future_days)

# Обучаем простую модель для тренда
model = LinearRegression()
model.fit(time_index.reshape(-1, 1), water_levels)
trend_pred = model.predict(future_index.reshape(-1, 1))

# Добавляем сезонную составляющую к прогнозу
seasonal_pred = 2 * np.sin(2 * np.pi * future_index / 365)
predicted_levels = trend_pred + seasonal_pred

# 3. Расчет стоимости токенов
# Формула: Price = Base_Price + (Level * Multiplier)
BASE_PRICE = 10.0
MULTIPLIER = 2.5

df['TokenPrice'] = BASE_PRICE + (df['WaterLevel'] * MULTIPLIER)
predicted_prices = BASE_PRICE + (predicted_levels * MULTIPLIER)

# 4. Геопространственная визуализация
# Координаты реки Баянколь (приблизительные для региона)
bayankol_coords = [45.5, 62.5] 

m = folium.Map(location=bayankol_coords, zoom_start=8, tiles='OpenStreetMap')

# Добавляем маркер станции мониторинга
folium.Marker(
    location=bayankol_coords,
    popup=f"Станция мониторинга Баянколь\nТекущий уровень: {df['WaterLevel'].iloc[-1]:.2f}м\nЦена токена: ${df['TokenPrice'].iloc[-1]:.2f}",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавляем круг влияния (зона мониторинга)
folium.Circle(
    location=bayankol_coords,
    radius=20000,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.2,
    popup='Зона влияния гидрологического узла'
).add_to(m)

m.save("264.html")

# 5. Визуализация графиков
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['WaterLevel'], label='Исторические данные', color='blue')
plt.plot(future_dates, predicted_levels, label='Прогноз', color='cyan', linestyle='--')
plt.title('Прогноз уровня воды в реке Баянколь')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['TokenPrice'], label='Историческая цена', color='green')
plt.plot(future_dates, predicted_prices, label='Прогноз цены', color='lime', linestyle='--')
plt.title('Прогноз стоимости токена (привязка к уровню воды)')
plt.ylabel('Цена ($)')
plt.xlabel('Дата')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("Моделирование завершено. Карта сохранена в файл 264.html")