import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Предположим, что у нас есть данные в формате CSV с датами и значениями
# Пример данных: date, snowfall, temperature, bayankol_water_level, lepsy_water_level

# Загрузка данных
data = pd.read_csv('snow_and_water_data.csv', parse_dates=['date'])
data.set_index('date', inplace=True)

# Предварительная обработка данных
data.fillna(method='ffill', inplace=True)  # Простое заполнение пропусков предыдущими значениями

# Вычисление индекса снеготаяния (простой пример: если температура > 0, то часть снега тает)
data['snowmelt_index'] = np.where(data['temperature'] > 0, data['snowfall'], 0)

# Корреляционный анализ
correlation_bayankol, _ = pearsonr(data['snowmelt_index'], data['bayankol_water_level'])
correlation_lepsy, _ = pearsonr(data['snowmelt_index'], data['lepsy_water_level'])

print(f'Корреляция между снеготаянием и уровнем воды в реке Bayankol: {correlation_bayankol}')
print(f'Корреляция между снеготаянием и уровнем воды в реке Lepsy: {correlation_lepsy}')

# Визуализация данных
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(data.index, data['snowmelt_index'], label='Индекс снеготаяния')
plt.plot(data.index, data['bayankol_water_level'], label='Уровень воды в реке Bayankol', alpha=0.7)
plt.title('Сравнение индекса снеготаяния и уровня воды в реке Bayankol')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(data.index, data['snowmelt_index'], label='Индекс снеготаяния')
plt.plot(data.index, data['lepsy_water_level'], label='Уровень воды в реке Lepsy', alpha=0.7)
plt.title('Сравнение индекса снеготаяния и уровня воды в реке Lepsy')
plt.legend()

plt.tight_layout()
plt.show()

# Визуализация на карте (пример координат для рек)
m = folium.Map(location=[45.0, 81.0], zoom_start=6)

folium.Marker([45.23, 79.87], popup='Bayankol River').add_to(m)
folium.Marker([45.15, 80.55], popup='Lepsy River').add_to(m)

m.save("162.html")