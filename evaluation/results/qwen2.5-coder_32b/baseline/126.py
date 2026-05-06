import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Предположим, что у нас есть CSV файлы с историческими данными о стоках рек
shilik_data = pd.read_csv('shilik_river_data.csv', parse_dates=['date'], index_col='date')
kishi_almaty_data = pd.read_csv('kishi_almaty_river_data.csv', parse_dates=['date'], index_col='date')

# Пример данных:
# shilik_river_data.csv
# date,discharge
# 2010-01-01,150.0
# 2010-01-02,148.0
# ...

# kishi_almaty_river_data.csv
# date,discharge
# 2010-01-01,130.0
# 2010-01-02,129.0
# ...

# Обработка данных: удаление пропусков и аномалий
shilik_data = shilik_data.dropna()
kishi_almaty_data = kishi_almaty_data.dropna()

# Анализ временных рядов для выявления сезонной составляющей
result_shilik = seasonal_decompose(shilik_data['discharge'], model='additive', period=12)
result_kishi_almaty = seasonal_decompose(kishi_almaty_data['discharge'], model='additive', period=12)

# Построение графиков сезонных изменений
plt.figure(figsize=(14, 8))

plt.subplot(2, 1, 1)
plt.plot(result_shilik.seasonal, label='Сезонная составляющая Шилик')
plt.title('Сезонные изменения уровня воды реки Шилик')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(result_kishi_almaty.seasonal, label='Сезонная составляющая Кыши Алматы', color='orange')
plt.title('Сезонные изменения уровня воды реки Кыши Алматы')
plt.legend()

plt.tight_layout()
plt.show()

# Географическая визуализация
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты Бишкека

# Добавление маркеров для рек
folium.Marker(
    location=[43.0000, 76.8500],
    popup='Река Шилик',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[42.9100, 75.2500],
    popup='Река Кыши Алматы',
    icon=folium.Icon(color='green')
).add_to(m)

# Сохранение карты
m.save("126.html")