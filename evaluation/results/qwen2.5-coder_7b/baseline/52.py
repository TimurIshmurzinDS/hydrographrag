import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'water_level': np.random.normal(loc=100, scale=10, size=365) + np.sin(np.linspace(0, 2*np.pi, 365)) * 50
}
df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Проверка данных на пропущенные значения
print(df.isnull().sum())

# Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['water_level'], label='Historical Water Level')
plt.title('Water Level of Sarykan River')
plt.xlabel('Date')
plt.ylabel('Water Level')
plt.legend()
plt.show()

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(df) * 0.8)
train, test = df[:train_size], df[train_size:]

# Обучение модели SARIMAX
model = SARIMAX(train['water_level'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 365))
results = model.fit()

# Прогнозирование на тестовую выборку
forecast = results.get_forecast(steps=len(test))
forecast_ci = forecast.conf_int()

# Визуализация прогноза
plt.figure(figsize=(12, 6))
plt.plot(train['water_level'], label='Train')
plt.plot(test['water_level'], label='Test', color='orange')
plt.plot(forecast.predicted_mean, label='Forecast', color='red')
plt.fill_between(forecast_ci.index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='pink', alpha=0.3)
plt.title('Water Level Forecast for Sarykan River')
plt.xlabel('Date')
plt.ylabel('Water Level')
plt.legend()
plt.show()

# Создание карты с прогнозами
m = folium.Map(location=[42.5, 76.1], zoom_start=8)

for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Water Level: {row['water_level']}", icon=folium.Icon(color='blue')).add_to(m)

# Добавление прогнозов на карту
for index, row in forecast.predicted_mean.iteritems():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Forecasted Water Level: {row['predicted_mean']}", icon=folium.Icon(color='red')).add_to(m)

m.save("52.html")