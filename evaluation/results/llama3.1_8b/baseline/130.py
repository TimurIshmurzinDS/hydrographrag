import pandas as pd
import numpy as np
from folium import Map, CircleMarker

# Загрузим данные о стоке реки Bayankol River и базовом уровне, установленном рекой Shilik River.
data = {
    'Дата': ['2020-01-01', '2020-02-01', '2020-03-01'],
    'Сток Байанкоула (м³/с)': [100, 120, 150],
    'Базовый уровень Шилика (м):' : [500, 520, 550]
}

df = pd.DataFrame(data)

# Рассчитаем историческое отклонение стока реки Bayankol River относительно базового уровня.
df['Отклонение'] = df['Сток Байанкоула (м³/с)'] - df['Базовый уровень Шилика (м):']

# Создадим карту с использованием библиотеки folium.
m = Map(location=[46.5, 76.0], zoom_start=10)

# Добавим маркеры на карте для каждого значения стока и базового уровня.
for index, row in df.iterrows():
    CircleMarker(
        location=[row['Дата'], row['Сток Байанкоула (м³/с)']],
        radius=row['Отклонение'],
        color='red'
    ).add_to(m)

# Сохраним карту как HTML-файл.
m.save("130.html")