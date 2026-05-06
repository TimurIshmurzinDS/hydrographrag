import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предположим, что у нас есть данные в формате CSV с колонками: 'date', 'Ili_River_Flow', 'Shyzhyn_River_Flow'
data = pd.read_csv('water_flow_data.csv', parse_dates=['date'], index_col='date')

# Проверка данных
print(data.head())

# Обработка пропусков (простое заполнение предыдущими значениями)
data.fillna(method='ffill', inplace=True)

# Анализ сезонности для реки Или
ili_decomposition = seasonal_decompose(data['Ili_River_Flow'], model='additive')
ili_seasonal = ili_decomposition.seasonal

# Анализ сезонности для реки Шызын
shyzhyn_decomposition = seasonal_decompose(data['Shyzhyn_River_Flow'], model='additive')
shyzhyn_seasonal = shyzhyn_decomposition.seasonal

# Построение графиков сезонных компонентов
plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
plt.plot(ili_seasonal.index, ili_seasonal.values, label='Сезонная составляющая Или')
plt.title('Сезонная составляющая расхода воды в реке Или')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(shyzhyn_seasonal.index, shyzhyn_seasonal.values, label='Сезонная составляющая Шызын', color='orange')
plt.title('Сезонная составляющая расхода воды в реке Шызын')
plt.legend()

plt.tight_layout()
plt.show()

# Создание карты с использованием folium
m = folium.Map(location=[45.3269, 71.8712], zoom_start=10)  # Координаты примерно посередине рек

# Добавление маркеров для мест измерений (примерные координаты)
folium.Marker([45.3269, 71.8712], popup='Или').add_to(m)  # Координаты примерные
folium.Marker([45.0833, 71.5833], popup='Шызын').add_to(m)  # Координаты примерные

# Сохранение карты в файл
m.save("160.html")