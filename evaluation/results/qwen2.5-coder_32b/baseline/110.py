import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Предположим, что данные о потоковом расходе воды и урожайности уже загружены в DataFrame
# Для примера создадим фиктивные данные
np.random.seed(0)
dates = pd.date_range(start='2020-01-01', end='2020-12-31')
sarykan_discharge = np.random.uniform(low=5, high=50, size=len(dates))
tekeli_discharge = np.random.uniform(low=3, high=40, size=len(dates))
crop_yield = np.random.uniform(low=1000, high=5000, size=len(dates))

data = pd.DataFrame({
    'Date': dates,
    'Sarykan_Discharge': sarykan_discharge,
    'Tekeli_Discharge': tekeli_discharge,
    'Crop_Yield': crop_yield
})

# Анализ временных рядов
plt.figure(figsize=(14, 7))
plt.plot(data['Date'], data['Sarykan_Discharge'], label='Расход воды в реке Sarykan')
plt.plot(data['Date'], data['Tekeli_Discharge'], label='Расход воды в реке Tekeli')
plt.xlabel('Дата')
plt.ylabel('Объем воды (куб. м/с)')
plt.title('Темповый ряд потокового расхода воды')
plt.legend()
plt.show()

# Соотнесение данных о воде и урожайности
correlation_sarykan, _ = pearsonr(data['Sarykan_Discharge'], data['Crop_Yield'])
correlation_tekeli, _ = pearsonr(data['Tekeli_Discharge'], data['Crop_Yield'])

print(f'Корреляция между расходом воды в реке Sarykan и урожайностью: {correlation_sarykan}')
print(f'Корреляция между расходом воды в реке Tekeli и урожайностью: {correlation_tekeli}')

# Визуализация на карте
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерно по центру Кыргызстана

folium.Marker(
    location=[43.0000, 75.0000],
    popup='Sarykan River',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[42.8000, 76.1000],
    popup='Tekeli River',
    icon=folium.Icon(color='green')
).add_to(m)

m.save("110.html")