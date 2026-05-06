import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium

# Предположим, что у нас есть CSV файлы с данными о уровнях воды для рек Koksu и Byzhy.
# Файлы должны содержать столбцы: 'date' (дата), 'water_level' (уровень воды).

# Загрузка данных
koksudata = pd.read_csv('koksudata.csv', parse_dates=['date'])
byzhydata = pd.read_csv('byzhydata.csv', parse_dates=['date'])

# Обработка данных: удаление пропусков и сортировка по дате
koksudata.dropna(inplace=True)
koksudata.sort_values(by='date', inplace=True)

byzhydata.dropna(inplace=True)
byzhydata.sort_values(by='date', inplace=True)

# Вычисление минимальных уровней воды для каждого года
koksu_min_levels = koksudata.resample('Y', on='date')['water_level'].min().reset_index()
byzhy_min_levels = byzhydata.resample('Y', on='date')['water_level'].min().reset_index()

# Анализ тренда с использованием линейной регрессии
slope_koksu, intercept_koksu, r_value_koksu, p_value_koksu, std_err_koksu = stats.linregress(koksu_min_levels['date'].map(pd.Timestamp.toordinal), koksu_min_levels['water_level'])
slope_byzhy, intercept_byzhy, r_value_byzhy, p_value_byzhy, std_err_byzhy = stats.linregress(byzhy_min_levels['date'].map(pd.Timestamp.toordinal), byzhy_min_levels['water_level'])

# Построение графиков
plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
plt.plot(koksu_min_levels['date'], koksu_min_levels['water_level'], label='Минимальный уровень воды')
plt.plot(koksu_min_levels['date'], slope_koksu * koksu_min_levels['date'].map(pd.Timestamp.toordinal) + intercept_koksu, color='red', label=f'Тренд (R² = {r_value_koksu**2:.2f})')
plt.title('Коксу Река')
plt.xlabel('Год')
plt.ylabel('Уровень воды')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(byzhy_min_levels['date'], byzhy_min_levels['water_level'], label='Минимальный уровень воды')
plt.plot(byzhy_min_levels['date'], slope_byzhy * byzhy_min_levels['date'].map(pd.Timestamp.toordinal) + intercept_byzhy, color='red', label=f'Тренд (R² = {r_value_byzhy**2:.2f})')
plt.title('Бызхы Река')
plt.xlabel('Год')
plt.ylabel('Уровень воды')
plt.legend()

plt.tight_layout()
plt.show()

# Визуализация на карте с использованием folium
m = folium.Map(location=[43.25, 79.8], zoom_start=10)

# Координаты рек (примерные)
koksu_coords = [43.26, 79.8]
byzhy_coords = [43.24, 79.7]

folium.Marker(koksu_coords, popup='Коксу Река').add_to(m)
folium.Marker(byzhy_coords, popup='Бызхы Река').add_to(m)

m.save("208.html")