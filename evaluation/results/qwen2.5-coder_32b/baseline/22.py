import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о уровне воды в реке Узын Каргалы.
# Файл содержит столбцы: 'date' (дата измерения) и 'water_level' (уровень воды).

data = pd.read_csv('uzyn_kargaly_water_levels.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Удаление пропусков и аномалий.
data.dropna(inplace=True)
# Предположим, что уровень воды не может быть отрицательным или слишком большим (например, более 10 метров).
data = data[(data['water_level'] >= 0) & (data['water_level'] <= 10)]

# Шаг 3: Анализ временных рядов
# Определение пикового уровня воды.
peak_water_level = data['water_level'].max()
peak_date = data.loc[data['water_level'].idxmax(), 'date']

print(f"Пиковый уровень воды в реке Узын Каргалы был {peak_water_level} метров, дата: {peak_date}")

# Шаг 4: Визуализация результатов
# Создание карты с помощью folium.
m = folium.Map(location=[50.2679, 83.1954], zoom_start=10)  # Координаты примерного местоположения реки Узын Каргалы

# Добавление маркера на карту с информацией о пиковом уровне воды.
folium.Marker(
    location=[50.2679, 83.1954],  # Координаты примерного местоположения реки Узын Каргалы
    popup=f"Пиковый уровень воды: {peak_water_level} м\nДата: {peak_date}",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в файл.
m.save("22.html")

# Дополнительно: Визуализация временного ряда для анализа
plt.figure(figsize=(14, 7))
plt.plot(data['date'], data['water_level'], label='Уровень воды')
plt.scatter(peak_date, peak_water_level, color='red', zorder=5, label=f'Пик: {peak_water_level} м\n{peak_date}')
plt.title('Уровень воды в реке Узын Каргалы во время весеннего паводка')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.legend()
plt.grid(True)
plt.show()