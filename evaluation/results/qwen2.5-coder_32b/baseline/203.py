import pandas as pd
import numpy as np
from scipy.stats import gumbel_r
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о уровне воды в реке Koksu
data = pd.read_csv('koksu_water_level.csv', parse_dates=['date'], index_col='date')

# Проверяем первые строки данных
print(data.head())

# Шаг 2: Анализ временного ряда
# Простой анализ для начала - построим график уровня воды
data.plot(title='Уровень воды в реке Koksu')
plt.show()

# Шаг 3: Определение порога 50-летнего паводка
# Используем метод Gumbel для оценки вероятностного распределения экстремальных значений
params = gumbel_r.fit(data['water_level'])
threshold_50_year_flood = gumbel_r.ppf(1 - 1/50, *params)

print(f'Порог 50-летнего паводка: {threshold_50_year_flood}')

# Шаг 4: Расчет вероятности превышения порога
# Рассчитаем вероятность того, что уровень воды превысит порог 50-летнего паводка
probability_exceedance = (data['water_level'] > threshold_50_year_flood).mean()
print(f'Вероятность превышения порога 50-летнего паводка: {probability_exceedance}')

# Шаг 5: Визуализация результатов
# Предположим, что у нас есть координаты реки Koksu
koksu_coords = [42.6389, 78.1806]  # примерные координаты

m = folium.Map(location=koksu_coords, zoom_start=10)

# Добавим маркер с информацией о вероятности превышения порога
folium.Marker(
    location=koksu_coords,
    popup=f'Вероятность превышения порога 50-летнего паводка: {probability_exceedance:.2f}',
    icon=folium.Icon(color='red')
).add_to(m)

# Сохраняем карту
m.save("203.html")