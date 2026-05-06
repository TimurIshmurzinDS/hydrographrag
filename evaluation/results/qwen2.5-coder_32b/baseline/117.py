import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предположим, что у нас есть временные ряды данных о стоке воды для рек Уржар и Аксу.
# Для примера создадим синтетические данные.

np.random.seed(0)
dates = pd.date_range(start='2010-01-01', end='2020-12-31')
urzhar_discharge = 50 + np.sin(np.linspace(0, 10*np.pi, len(dates))) * 10 + np.random.normal(0, 1, len(dates))
aksu_discharge = 40 + np.cos(np.linspace(0, 10*np.pi, len(dates))) * 8 + np.random.normal(0, 1, len(dates))

discharge_data = pd.DataFrame({
    'Date': dates,
    'Urzhar_Discharge': urzhar_discharge,
    'Aksu_Discharge': aksu_discharge
})

# Анализ временных рядов с использованием декомпозиции на тренд, сезонность и остатки.
urzhar_decomposition = seasonal_decompose(discharge_data['Urzhar_Discharge'], model='additive', period=12)
aksu_decomposition = seasonal_decompose(discharge_data['Aksu_Discharge'], model='additive', period=12)

# Построение графиков для визуализации трендов и сезонности.
plt.figure(figsize=(14, 8))

plt.subplot(311)
plt.plot(urzhar_discharge, label='Urzhar Discharge')
plt.title('Тренд и сезонность стока воды реки Уржар')
plt.legend()

plt.subplot(312)
plt.plot(urzhar_decomposition.trend, label='Trend', color='orange')
plt.legend()

plt.subplot(313)
plt.plot(urzhar_decomposition.seasonal, label='Seasonality', color='green')
plt.legend()

plt.tight_layout()
plt.show()

# Аналогично для реки Аксу.
plt.figure(figsize=(14, 8))

plt.subplot(311)
plt.plot(aksu_discharge, label='Aksu Discharge')
plt.title('Тренд и сезонность стока воды реки Аксу')
plt.legend()

plt.subplot(312)
plt.plot(aksu_decomposition.trend, label='Trend', color='orange')
plt.legend()

plt.subplot(313)
plt.plot(aksu_decomposition.seasonal, label='Seasonality', color='green')
plt.legend()

plt.tight_layout()
plt.show()

# Предположим, что мы моделируем экологический дисбаланс как функцию от изменения стока воды.
# Для простоты используем линейную модель.

def ecological_disbalance(discharge):
    return 0.5 * discharge - 20

discharge_data['Urzhar_Disbalance'] = ecological_disbalance(urzhar_discharge)
discharge_data['Aksu_Disbalance'] = ecological_disbalance(aksu_discharge)

# Визуализация экологического дисбаланса.
plt.figure(figsize=(14, 6))
plt.plot(discharge_data['Date'], discharge_data['Urzhar_Disbalance'], label='Уржар', color='blue')
plt.plot(discharge_data['Date'], discharge_data['Aksu_Disbalance'], label='Аксу', color='red')
plt.title('Экологический дисбаланс рек Уржар и Аксу')
plt.xlabel('Дата')
plt.ylabel('Дисбаланс')
plt.legend()
plt.show()

# Предположим, что мы имеем географические данные о местоположении точек наблюдения.
# Для примера создадим синтетические координаты.

locations = {
    'Urzhar': [45.0328, 76.9158],  # Примерные координаты Уржара
    'Aksu': [42.8743, 78.2932]     # Примерные координаты Аксу
}

# Создание карты с отображением зон риска.
m = folium.Map(location=[43.5, 77.5], zoom_start=6)

for river, coords in locations.items():
    disbalance_value = discharge_data[f'{river}_Disbalance'].iloc[-1]  # Последнее значение дисбаланса
    color = 'green' if disbalance_value < 0 else ('yellow' if disbalance_value < 5 else 'red')
    
    folium.Marker(
        location=coords,
        popup=f'{river} Дисбаланс: {disbalance_value:.2f}',
        icon=folium.Icon(color=color)
    ).add_to(m)

m.save("117.html")