import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import folium

# Предположим, что у нас есть временные ряды уровней воды для двух рек в формате CSV.
# Файлы должны содержать столбцы: 'date' (дата), 'level' (уровень воды).

# Загрузка данных
bayankol_data = pd.read_csv('bayankol_water_level.csv', parse_dates=['date'])
lepsy_data = pd.read_csv('lepsy_water_level.csv', parse_dates=['date'])

# Предварительная обработка данных: удаление пропусков и сортировка по дате
bayankol_data.dropna(inplace=True)
bayankol_data.sort_values(by='date', inplace=True)

lepsy_data.dropna(inplace=True)
lepsy_data.sort_values(by='date', inplace=True)

# Определение периода весеннего половодья (например, с марта по апрель)
spring_start = pd.Timestamp('2023-03-01')
spring_end = pd.Timestamp('2023-04-30')

bayankol_spring = bayankol_data[(bayankol_data['date'] >= spring_start) & (bayankol_data['date'] <= spring_end)]
lepsy_spring = lepsy_data[(lepsy_data['date'] >= spring_start) & (lepsy_data['date'] <= spring_end)]

# Поиск пиков уровней воды
bayankol_peaks, _ = find_peaks(bayankol_spring['level'], height=0)
lepsy_peaks, _ = find_peaks(lepsy_spring['level'], height=0)

# Определение максимального уровня воды и соответствующей даты
bayankol_max_peak = bayankol_spring.iloc[bayankol_peaks[np.argmax(bayankol_spring['level'].iloc[bayankol_peaks])]]
lepsy_max_peak = lepsy_spring.iloc[lepsy_peaks[np.argmax(lepsy_spring['level'].iloc[lepsy_peaks])]]

# Визуализация данных
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(bayankol_spring['date'], bayankol_spring['level'], label='Уровень воды')
plt.scatter(bayankol_max_peak['date'], bayankol_max_peak['level'], color='red', label='Максимальный уровень')
plt.title('Динамика уровня воды реки Bayankol (весна 2023)')
plt.xlabel('Дата')
plt.ylabel('Уровень воды, м')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(lepsy_spring['date'], lepsy_spring['level'], label='Уровень воды')
plt.scatter(lepsy_max_peak['date'], lepsy_max_peak['level'], color='red', label='Максимальный уровень')
plt.title('Динамика уровня воды реки Lepsy (весна 2023)')
plt.xlabel('Дата')
plt.ylabel('Уровень воды, м')
plt.legend()

plt.tight_layout()
plt.show()

# Создание карты с отметками уровней воды
m = folium.Map(location=[45.0, 81.0], zoom_start=6)  # Координаты примерные

folium.Marker(
    location=[bayankol_max_peak['latitude'], bayankol_max_peak['longitude']],
    popup=f"Bayankol River\nДата: {bayankol_max_peak['date']}\nУровень воды: {bayankol_max_peak['level']} м",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[lepsy_max_peak['latitude'], lepsy_max_peak['longitude']],
    popup=f"Lepsy River\nДата: {lepsy_max_peak['date']}\nУровень воды: {lepsy_max_peak['level']} м",
    icon=folium.Icon(color='green')
).add_to(m)

m.save("155.html")