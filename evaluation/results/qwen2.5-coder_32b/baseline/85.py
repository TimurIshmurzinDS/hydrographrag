import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import folium

# Предположим, что у нас есть CSV файлы с данными о расходе воды на реках
# Эти данные должны содержать столбцы: 'date', 'discharge' (расход воды)

# Загрузка данных
koktal_data = pd.read_csv('koktal_discharge.csv', parse_dates=['date'])
baskan_data = pd.read_csv('baskan_discharge.csv', parse_dates=['date'])

# Интерполяция пропущенных значений, если необходимо
koktal_data['discharge'] = koktal_data['discharge'].interpolate()
baskan_data['discharge'] = baskan_data['discharge'].interpolate()

# Анализ сезонных паттернов
koktal_monthly_avg = koktal_data.resample('M', on='date').mean()
baskan_monthly_avg = baskan_data.resample('M', on='date').mean()

# Построение графиков для визуализации сезонных изменений
plt.figure(figsize=(14, 7))
plt.plot(koktal_monthly_avg.index, koktal_monthly_avg['discharge'], label='Koktal River')
plt.plot(baskan_monthly_avg.index, baskan_monthly_avg['discharge'], label='Baskan River')
plt.title('Сезонные изменения расхода воды на реках Koktal и Baskan')
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.legend()
plt.grid(True)
plt.show()

# Определение пороговых значений для риска затопления
# Предположим, что если расход превышает определенное значение, есть риск затопления
threshold_koktal = koktal_monthly_avg['discharge'].mean() + 2 * koktal_monthly_avg['discharge'].std()
threshold_baskan = baskan_monthly_avg['discharge'].mean() + 2 * baskan_monthly_avg['discharge'].std()

# Определение периодов риска затопления
risk_periods_koktal = koktal_data[koktal_data['discharge'] > threshold_koktal]
risk_periods_baskan = baskan_data[baskan_data['discharge'] > threshold_baskan]

# Создание карты с использованием folium
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерно по центру Кыргызстана

# Добавление маркеров для точек риска затопления
for idx, row in risk_periods_koktal.iterrows():
    folium.Marker(
        location=[42.8746, 74.5910],  # Координаты реки Koktal (примерные)
        popup=f"Koktal River: {row['discharge']} куб. м/с",
        icon=folium.Icon(color='red')
    ).add_to(m)

for idx, row in risk_periods_baskan.iterrows():
    folium.Marker(
        location=[42.8746, 74.5910],  # Координаты реки Baskan (примерные)
        popup=f"Baskan River: {row['discharge']} куб. м/с",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("85.html")