import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import folium

# Предположим, что у нас есть CSV файл с данными о расходе воды в реке Kurty River.
# Файл должен содержать столбцы: 'date' (дата) и 'discharge' (расход воды).

# Шаг 1: Сбор данных
data = pd.read_csv('kurty_river_discharge.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
data.set_index('date', inplace=True)

# Шаг 3: Разделение данных на периоды (летний - июнь, июль, август; зимний - декабрь, январь, февраль)
summer_data = data[(data.index.month >= 6) & (data.index.month <= 8)]
winter_data = data[(data.index.month == 12) | (data.index.month.isin([1, 2]))]

# Шаг 4: Вычисление средних значений
mean_summer_discharge = summer_data['discharge'].mean()
mean_winter_discharge = winter_data['discharge'].mean()

print(f"Средний расход воды в летний период: {mean_summer_discharge} м³/с")
print(f"Средний расход воды в зимний период: {mean_winter_discharge} м³/с")

# Шаг 5: Визуализация результатов
plt.figure(figsize=(10, 6))
summer_data['discharge'].resample('M').mean().plot(label='Летний период', color='orange')
winter_data['discharge'].resample('M').mean().plot(label='Зимний период', color='blue')
plt.title('Среднемесячный расход воды в реке Kurty River')
plt.xlabel('Дата')
plt.ylabel('Расход воды, м³/с')
plt.legend()
plt.grid(True)
plt.show()

# Шаг 6: Географическая визуализация (опционально)
# Предположим, что у нас есть координаты местности реки.
map_center = [51.8329, 47.0912]  # Примерные координаты реки Kurty River
m = folium.Map(location=map_center, zoom_start=10)

# Добавление маркера на карту (пример)
folium.Marker(
    location=[51.8329, 47.0912],
    popup='Куртская река',
    icon=folium.Icon(color='blue')
).add_to(m)

m.save("51.html")