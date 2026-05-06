import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 1. Симуляция данных (так как реальный датасет Shyzhyn River недоступен)
# Создаем временной ряд за 5 лет с выраженной сезонностью
np.random.seed(42)
dates = pd.date_range(start="2018-01-01", end="2022-12-31", freq='M')
n = len(dates)

# Базовый расход + сезонный синус (пик весной) + шум
base_flow = 15.0
seasonal_pattern = 10 * np.sin(2 * np.pi * np.arange(n) / 12 - np.pi/2)
noise = np.random.normal(0, 2, n)
discharge_values = base_flow + seasonal_pattern + noise

df = pd.DataFrame({'Date': dates, 'Discharge': discharge_values})
df.set_index('Date', inplace=True)

# 2. Сезонная декомпозиция
decomposition = seasonal_decompose(df['Discharge'], model='additive')
fig_decomp = decomposition.plot()
plt.suptitle("Seasonal Decomposition of Shyzhyn River Discharge", y=1.02)
plt.show()

# 3. Моделирование SARIMA
# Разделение на train и test (последние 12 месяцев для проверки)
train = df.iloc[:-12]
test = df.iloc[-12:]

# Параметры SARIMA (p,d,q) x (P,D,Q,s)
# s=12 для месячных данных
model = SARIMAX(train['Discharge'], 
                order=(1, 1, 1), 
                seasonal_order=(1, 1, 1, 12), 
                enforce_stationarity=False, 
                enforce_invertibility=False)
results = model.fit(disp=False)

# Прогноз на 12 месяцев
forecast = results.get_forecast(steps=12)
forecast_mean = forecast.predicted_mean
conf_int = forecast.conf_int()

# 4. Верификация
rmse = np.sqrt(mean_squared_error(test['Discharge'], forecast_mean))
mae = mean_absolute_error(test['Discharge'], forecast_mean)

print(f"Verification Metrics:\nRMSE: {rmse:.3f}\nMAE: {mae:.3f}")

# Визуализация прогноза
plt.figure(figsize=(12, 6))
plt.plot(train.index, train['Discharge'], label='Train')
plt.plot(test.index, test['Discharge'], label='Actual (Test)', color='blue')
plt.plot(test.index, forecast_mean, label='Forecast', color='red')
plt.fill_between(test.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)
plt.title("Seasonal Water Discharge Forecast: Shyzhyn River")
plt.legend()
plt.grid(True)
plt.show()

# 5. Геопространственная визуализация (Folium)
# Координаты (условные для Shyzhyn River)
river_coords = [
    [50.123, 35.456], [50.130, 35.470], [50.145, 35.485], 
    [50.160, 35.500], [50.180, 35.520], [50.200, 35.550]
]
station_coord = [50.160, 35.500]

m = folium.Map(location=[50.160, 35.500], zoom_start=12, tiles='OpenStreetMap')

# Рисуем русло реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Shyzhyn River").add_to(m)

# Добавляем маркер станции мониторинга
folium.Marker(
    location=station_coord,
    popup=f"Monitoring Station\nRMSE: {rmse:.2f}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("21.html")
print("Map has been saved as 21.html")