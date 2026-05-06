import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import find_peaks
import folium

# Предположим, что у нас есть данные о расходе воды в файле 'turgen_river_flow.csv'
# Структура файла: дата (date), расход воды (flow)

# Шаг 1: Загрузка данных
data = pd.read_csv('turgen_river_flow.csv', parse_dates=['date'], index_col='date')

# Шаг 2: Предварительная обработка данных
data.dropna(inplace=True)  # Удаление пропусков

# Шаг 3: Анализ временных рядов
decomposition = seasonal_decompose(data['flow'], model='additive', period=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Нормализация данных для поиска пиков
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data[['flow']])
peaks, _ = find_peaks(scaled_data.flatten(), height=0.8)  # Поиск пиков с высотой > 0.8

# Шаг 4: Визуализация результатов
plt.figure(figsize=(12, 8))
plt.subplot(411)
plt.plot(data['flow'], label='Исходные данные')
plt.legend(loc='best')

plt.subplot(412)
plt.plot(trend, label='Тренд')
plt.legend(loc='best')

plt.subplot(413)
plt.plot(seasonal,label='Сезонность')
plt.legend(loc='best')

plt.subplot(414)
plt.plot(residual, label='Остатки')
plt.scatter(data.index[peaks], data['flow'].iloc[peaks], color='red', label='Пики (возможные паводки)')
plt.legend(loc='best')

plt.tight_layout()
plt.show()

# Шаг 5: Визуализация на карте
# Предположим, что у нас есть координаты реки Turgen River
m = folium.Map(location=[42.8746, 78.2932], zoom_start=10)  # Координаты примерные

for peak in peaks:
    date = data.index[peak]
    flow_value = data['flow'].iloc[peak]
    folium.Marker(
        location=[42.8746, 78.2932],  # Координаты примерные
        popup=f'Дата: {date}, Расход воды: {flow_value}',
        icon=folium.Icon(color='red')
    ).add_to(m)

m.save("79.html")