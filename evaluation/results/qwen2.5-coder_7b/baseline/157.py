import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'shilik_river': np.sin(np.linspace(0, 4 * np.pi, 365)) + np.random.normal(0, 0.1, 365),
    'shyzhyn_river': np.cos(np.linspace(0, 4 * np.pi, 365)) + np.random.normal(0, 0.1, 365)
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Анализ временных рядов
def analyze_time_series(df):
    for column in df.columns:
        plt.figure(figsize=(12, 4))
        plt.plot(df[column], label=column)
        plot_acf(df[column], lags=20, ax=plt.subplot(1, 2, 1), title=f'ACF {column}')
        plot_pacf(df[column], lags=20, ax=plt.subplot(1, 2, 2), title=f'PACF {column}')
        plt.tight_layout()
        plt.show()

analyze_time_series(df)

# Прогнозирование с помощью ARIMA
def fit_arima_model(series, order):
    model = ARIMA(series, order=order)
    result = model.fit()
    return result

arima_order = (1, 1, 1)  # Параметры ARIMA (p,d,q)

shilik_river_model = fit_arima_model(df['shilik_river'], arima_order)
shyzhyn_river_model = fit_arima_model(df['shyzhyn_river'], arima_order)

# Прогнозирование на следующие 30 дней
forecast_steps = 30

shilik_river_forecast = shilik_river_model.forecast(steps=forecast_steps)
shyzhyn_river_forecast = shyzhyn_river_model.forecast(steps=forecast_steps)

# Визуализация прогнозов на карте
m = folium.Map(location=[52.0, 86.0], zoom_start=4)  # Пример координат для России

folium.Marker([52.0, 86.0], popup='Shilik River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([51.0, 76.0], popup='Shyzhyn River', icon=folium.Icon(color='red')).add_to(m)

for i in range(forecast_steps):
    folium.CircleMarker(
        location=[52.0 + np.random.uniform(-0.1, 0.1), 86.0 + np.random.uniform(-0.1, 0.1)],
        radius=shilik_river_forecast[i] * 10,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

    folium.CircleMarker(
        location=[51.0 + np.random.uniform(-0.1, 0.1), 76.0 + np.random.uniform(-0.1, 0.1)],
        radius=shyzhyn_river_forecast[i] * 10,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

m.save("157.html")