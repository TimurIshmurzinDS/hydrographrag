import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предполагаем, что данные находятся в CSV файлах с колонками 'date' и 'discharge'
temirlik_data = pd.read_csv('temirlik_discharge.csv', parse_dates=['date'])
turgun_data = pd.read_csv('turgun_discharge.csv', parse_dates=['date'])

# Обработка данных
temirlik_data.dropna(inplace=True)
turgun_data.dropna(inplace=True)

# Анализ сезонности с использованием seasonal_decompose
temirlik_decomposed = seasonal_decompose(temirlik_data['discharge'], model='additive', period=12)
turgun_decomposed = seasonal_decompose(turgun_data['discharge'], model='additive', period=12)

# Построение графиков сезонных динамик
plt.figure(figsize=(14, 8))

plt.subplot(2, 1, 1)
temirlik_decomposed.seasonal.plot()
plt.title('Сезонная динамика расхода воды на Темирлик Реке')
plt.xlabel('Время')
plt.ylabel('Расход воды')

plt.subplot(2, 1, 2)
turgun_decomposed.seasonal.plot(color='orange')
plt.title('Сезонная динамика расхода воды на Турген Реке')
plt.xlabel('Время')
plt.ylabel('Расход воды')

plt.tight_layout()
plt.show()

# Оценка угрозы весенних наводнений
temirlik_max = temirlik_data[temirlik_data['date'].dt.month.isin([3, 4, 5])]['discharge'].max()
turgun_max = turgun_data[turgun_data['date'].dt.month.isin([3, 4, 5])]['discharge'].max()

print(f"Максимальный расход воды на Темирлик Реке в весенний период: {temirlik_max}")
print(f"Максимальный расход воды на Турген Реке в весенний период: {turgun_max}")

# Создание интерактивной карты с отметками местоположений рек
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерные

folium.Marker(
    location=[42.8746, 74.5910],
    popup='Темирлик Река',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[43.0000, 74.5000],  # Координаты примерные
    popup='Турген Река',
    icon=folium.Icon(color='green')
).add_to(m)

m.save("83.html")