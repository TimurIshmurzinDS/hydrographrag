import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2018', end='12/31/2022'),
    'Baskan_River': np.random.randint(50, 200, size=730),
    'Prokhodnaya_River': np.random.randint(40, 180, size=730)
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Построение временных рядов
plt.figure(figsize=(12, 6))
plt.plot(df['Baskan_River'], label='Baskan River')
plt.plot(df['Prokhodnaya_River'], label='Prokhodnaya River')
plt.title('Сезонный расход воды на реках Baskan и Prokhodnaya')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3)')
plt.legend()
plt.show()

# Декомпозиция временных рядов
decompose_baskan = seasonal_decompose(df['Baskan_River'], model='additive', period=12)
decompose_prokhodnaya = seasonal_decompose(df['Prokhodnaya_River'], model='additive', period=12)

# Визуализация декомпозиции
plt.figure(figsize=(12, 6))
decompose_baskan.plot()
plt.title('Декомпозиция сезонного расхода воды на Baskan River')
plt.show()

plt.figure(figsize=(12, 6))
decompose_prokhodnaya.plot()
plt.title('Декомпозиция сезонного расхода воды на Prokhodnaya River')
plt.show()

# Прогнозирование весеннего половодья
from statsmodels.tsa.arima.model import ARIMA

model_baskan = ARIMA(df['Baskan_River'], order=(5,1,0))
model_prokhodnaya = ARIMA(df['Prokhodnaya_River'], order=(5,1,0))

model_baskan_fit = model_baskan.fit()
model_prokhodnaya_fit = model_prokhodnaya.fit()

forecast_baskan = model_baskan_fit.forecast(steps=30)
forecast_prokhodnaya = model_prokhodnaya_fit.forecast(steps=30)

# Визуализация прогнозов
plt.figure(figsize=(12, 6))
plt.plot(df['Baskan_River'], label='Исторический расход Baskan River')
plt.plot(forecast_baskan, label='Прогноз Baskan River', color='red')
plt.title('Прогноз сезонного расхода воды на Baskan River')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['Prokhodnaya_River'], label='Исторический расход Prokhodnaya River')
plt.plot(forecast_prokhodnaya, label='Прогноз Prokhodnaya River', color='red')
plt.title('Прогноз сезонного расхода воды на Prokhodnaya River')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3)')
plt.legend()
plt.show()

# Создание карты для визуализации прогнозов
m = folium.Map(location=[50.45, 87.12], zoom_start=6)

folium.Marker([50.45, 87.12], popup='Baskan River').add_to(m)
folium.Marker([50.45, 87.13], popup='Prokhodnaya River').add_to(m)

for i in range(len(forecast_baskan)):
    folium.CircleMarker(
        location=[50.45, 87.12],
        radius=forecast_baskan[i] / 100,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

for i in range(len(forecast_prokhodnaya)):
    folium.CircleMarker(
        location=[50.45, 87.13],
        radius=forecast_prokhodnaya[i] / 100,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

m.save("77.html")