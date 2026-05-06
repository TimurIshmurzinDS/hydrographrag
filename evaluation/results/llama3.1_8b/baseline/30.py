import pandas as pd
import numpy as np
from folium import Map, Marker

# Подготовка данных (предположим, что у нас есть данные о расходе воды за последние несколько лет)
data = {
    'Дата': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01'],
    'Расход (м³/с)': [10, 15, 20, 25, 30]
}
df = pd.DataFrame(data)

# Обработка данных
mean_flow = df['Расход (м³/с)'].mean()
print(f'Средний расход: {mean_flow} м³/с')

# Рассчет индекса риска наводнения
current_flow = 25  # Текущий расход воды в реке Прохождение
risk_index = (current_flow - mean_flow) / mean_flow * 100
print(f'Индекс риска наводнения: {risk_index}%')

# Визуализация результатов на карте
m = Map(location=[55.7558, 37.6173], zoom_start=10)
Marker(location=[55.7558, 37.6173], popup=f'Река Прохождение\nИндекс риска наводнения: {risk_index}%').add_to(m)

# Сохранение карты в файл
m.save("30.html")