import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предполагается, что данные находятся в CSV файлах с колонками 'date' и 'discharge'
koksudata = pd.read_csv('koksudischarge.csv', parse_dates=['date'])
emeldata = pd.read_csv('emeldischarge.csv', parse_dates=['date'])

# Обработка данных
koksudata.dropna(inplace=True)
emeldata.dropna(inplace=True)

# Ограничение временного периода до последних 10 лет
end_date = koksudata['date'].max()
start_date = end_date - pd.DateOffset(years=10)
koksudata = koksudata[(koksudata['date'] >= start_date) & (koksudata['date'] <= end_date)]
emeldata = emeldata[(emeldata['date'] >= start_date) & (emeldata['date'] <= end_date)]

# Анализ сезонных закономерностей
koksudecomp = seasonal_decompose(koksudata.set_index('date')['discharge'], model='additive', period=12)
emeldecomp = seasonal_decompose(emeldata.set_index('date')['discharge'], model='additive', period=12)

# Построение графиков
plt.figure(figsize=(14, 8))

plt.subplot(2, 2, 1)
plt.plot(koksudata['date'], koksudata['discharge'])
plt.title('Расход воды в реке Koksu')
plt.xlabel('Дата')
plt.ylabel('Расход воды')

plt.subplot(2, 2, 2)
plt.plot(emeldata['date'], emeldata['discharge'])
plt.title('Расход воды в реке Emel')
plt.xlabel('Дата')
plt.ylabel('Расход воды')

plt.subplot(2, 2, 3)
koksudecomp.seasonal.plot()
plt.title('Сезонная составляющая Koksu')

plt.subplot(2, 2, 4)
emeldecomp.seasonal.plot()
plt.title('Сезонная составляющая Emel')

plt.tight_layout()
plt.show()

# Создание карты с местоположениями рек
m = folium.Map(location=[43.0651, 79.8922], zoom_start=8)  # Координаты примерно по центру Кыргызстана

folium.Marker(
    location=[42.9833, 80.2833],
    popup='Koksu River',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[41.6572, 80.2156],
    popup='Emel River',
    icon=folium.Icon(color='green')
).add_to(m)

m.save("196.html")