import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о расходе воды в реке Batareyka River.
# Файл содержит столбцы: 'date' (дата), 'discharge' (расход воды).

data = pd.read_csv('batareyka_river_discharge.csv', parse_dates=['date'])
data.set_index('date', inplace=True)

# Шаг 2: Предварительная обработка данных
# Проверка на пропуски и аномалии.
data.dropna(inplace=True)
z_scores = np.abs(stats.zscore(data['discharge']))
filtered_data = data[z_scores < 3]  # Удаление значений с Z-оценкой > 3

# Шаг 3: Определение периода паводка
# Предположим, что паводок определяется как период, когда расход воды превышает среднее значение на стандартное отклонение.
mean_discharge = filtered_data['discharge'].mean()
std_dev_discharge = filtered_data['discharge'].std()

flood_periods = filtered_data[filtered_data['discharge'] > (mean_discharge + std_dev_discharge)]

# Шаг 4: Анализ изменений расхода воды
# Построение графика временного ряда для всего периода и отдельно для паводков.
plt.figure(figsize=(12, 6))
plt.plot(filtered_data.index, filtered_data['discharge'], label='Расход воды')
plt.scatter(flood_periods.index, flood_periods['discharge'], color='red', label='Паводок')
plt.title('Изменения расхода воды в реке Batareyka River')
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.legend()
plt.show()

# Шаг 5: Визуализация результатов
# Предположим, что у нас есть координаты мест измерений расхода воды.
coordinates = [(43.2067, 44.9818), (43.2100, 44.9850)]  # Примерные координаты

m = folium.Map(location=[43.2067, 44.9818], zoom_start=12)

for coord in coordinates:
    folium.Marker(coord).add_to(m)

# Добавление слоя с тепловой картой для наглядности (опционально)
heat_data = [[coord[0], coord[1]] for coord in coordinates]
folium.plugins.HeatMap(heat_data).add_to(m)

m.save("20.html")