import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть временные ряды уровня воды для рек Shilik River и Shyzhyn River
# В реальности данные нужно будет загрузить из внешних источников
data = {
    'date': pd.date_range(start='2015-01-01', periods=730, freq='D'),
    'shilik_water_level': np.random.normal(loc=1.5, scale=0.5, size=730),
    'shyzhyn_water_level': np.random.normal(loc=1.2, scale=0.4, size=730)
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Функция для прогнозирования амплитуды сезонного стока
def forecast_seasonal_amplitude(series):
    # Разложение временного ряда на компоненты
    model = SARIMAX(series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 365))
    results = model.fit(disp=False)
    
    # Прогнозирование следующего года
    forecast = results.get_forecast(steps=365).predicted_mean
    
    # Вычисление амплитуды сезонного стока
    seasonal_amplitude = np.max(forecast) - np.min(forecast)
    return seasonal_amplitude

# Прогнозирование для рек Shilik River и Shyzhyn River
shilik_amplitude = forecast_seasonal_amplitude(df['shilik_water_level'])
shyzhyn_amplitude = forecast_seasonal_amplitude(df['shyzhyn_water_level'])

print(f"Прогнозируемая амплитуда сезонного стока для реки Shilik: {shilik_amplitude:.2f}")
print(f"Прогнозируемая амплитуда сезонного стока для реки Shyzhyn: {shyzhyn_amplitude:.2f}")

# Визуализация на карте с использованием folium
m = folium.Map(location=[50.45, 30.52], zoom_start=6)

# Координаты рек (примерные)
shilik_coords = [51.8975, 47.25]
shyzhyn_coords = [51.8975, 47.25]

folium.Marker(shilik_coords, popup=f"Shilik River\nАмплитуда: {shilik_amplitude:.2f}").add_to(m)
folium.Marker(shyzhyn_coords, popup=f"Shyzhyn River\nАмплитуда: {shyzhyn_amplitude:.2f}").add_to(m)

m.save("157.html")