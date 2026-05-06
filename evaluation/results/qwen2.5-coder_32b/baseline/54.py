import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о расходе воды в реке Karkara River.
# Файл содержит столбцы 'date' (дата) и 'discharge' (расход воды).

data = pd.read_csv('karkara_river_discharge.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Удаление пропусков и аномалий.
data.dropna(subset=['discharge'], inplace=True)
data = data[data['discharge'] > 0]  # Предположим, что отрицательные значения являются ошибочными.

# Шаг 3: Анализ данных
# Разделение данных на два десятилетия.
last_decade_start = pd.Timestamp('2010-01-01')
previous_decade_end = pd.Timestamp('2009-12-31')

data_last_decade = data[data['date'] >= last_decade_start]
data_previous_decade = data[data['date'] <= previous_decade_end]

# Расчет среднего значения расхода воды для каждого десятилетия.
mean_discharge_last_decade = data_last_decade['discharge'].mean()
mean_discharge_previous_decade = data_previous_decade['discharge'].mean()

# Шаг 4: Расчет разницы
difference_in_discharge = mean_discharge_last_decade - mean_discharge_previous_decade

print(f"Средний расход воды в последнем десятилетии: {mean_discharge_last_decade:.2f} м³/с")
print(f"Средний расход воды в предыдущем десятилетии: {mean_discharge_previous_decade:.2f} м³/с")
print(f"Разница в расходе воды: {difference_in_discharge:.2f} м³/с")

# Шаг 5: Визуализация результатов
# Предположим, что у нас есть координаты реки Karkara River.
karkara_river_coords = [43.1879, 69.0921]  # Примерные координаты

m = folium.Map(location=karkara_river_coords, zoom_start=10)

# Добавление маркера с информацией о разнице в расходе воды
folium.Marker(
    location=karkara_river_coords,
    popup=f"Разница в расходе воды: {difference_in_discharge:.2f} м³/с",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("54.html")