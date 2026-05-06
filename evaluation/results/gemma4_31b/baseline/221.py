import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import folium

# 1. Генерация синтетических данных (имитация уровня воды в реке Dos)
np.random.seed(42)
date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
n_days = len(date_range)

# Создаем тренд + сезонность (синус) + шум
trend = np.linspace(1.0, 2.5, n_days)  # Постепенный подъем
seasonality = 0.5 * np.sin(2 * np.pi * np.arange(n_days) / 365)
noise = np.random.normal(0, 0.1, n_days)
water_levels = trend + seasonality + noise

df = pd.DataFrame({'Date': date_range, 'WaterLevel': water_levels})

# 2. Подготовка данных для моделирования
# Преобразуем даты в числовой формат (дни с начала периода)
df['DayIndex'] = (df['Date'] - df['Date'].min()).dt.days
X = df[['DayIndex']].values
y = df['WaterLevel'].values

# 3. Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# 4. Предсказание на будущие 30 дней
future_days = 30
last_day = df['DayIndex'].max()
X_future = np.arange(last_day + 1, last_day + 1 + future_days).reshape(-1, 1)
y_future = model.predict(X_future)

# Создание дат для будущих прогнозов
future_dates = pd.date_range(start=df['Date'].max() + timedelta(days=1), periods=future_days)
df_future = pd.DataFrame({'Date': future_dates, 'WaterLevel': y_future})

# Визуализация графика
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['WaterLevel'], label='Исторические данные', color='blue')
plt.plot(df_future['Date'], df_future['WaterLevel'], label='Прогноз (Тренд)', color='red', linestyle='--')
plt.title('Прогноз уровня воды в реке Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Геопространственная визуализация (GIS)
# Предположим координаты станции мониторинга на реке Dos
# (Координаты выбраны условно для демонстрации)
lat, lon = 45.523062, -122.676482 

m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)

# Добавляем маркер станции мониторинга
folium.Marker(
    [lat, lon],
    popup=f"Станция мониторинга Dos River\nТекущий уровень: {df['WaterLevel'].iloc[-1]:.2f}м\nПрогноз на 30 дней: {'Рост' if y_future[-1] > y_future[0] else 'Спад'}",
    tooltip="Dos River Water Level Station",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавляем текстовое описание на карту
folium.Marker(
    [lat + 0.01, lon + 0.01],
    icon=folium.DivIcon(html=f"""<div style="font-family: Arial; color: black; font-weight: bold; background: white; padding: 5px; border: 1px solid black;">
                                    Прогноз уровня воды: {y_future[-1]:.2f} м.</div>""")
).add_to(m)

# Сохранение карты строго в файл 221.html
m.save("221.html")

print("Моделирование завершено. Прогноз построен, карта сохранена в файл 221.html")