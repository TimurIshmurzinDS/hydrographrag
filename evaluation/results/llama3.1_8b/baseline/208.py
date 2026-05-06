import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from folium import Map, Marker

# Загрузите данные о уровнях воды в реках Koksu и Byzhy за последние 10 лет.
data = {
    'Дата': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
             '2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01'],
    'Уровень воды в Koksu River': [5.2, 4.8, 6.1, 7.3, 8.5, 9.2, 10.1, 11.3, 12.5, 13.2],
    'Уровень воды в Byzhy River': [3.5, 4.1, 5.3, 6.5, 7.7, 8.4, 9.3, 10.5, 11.7, 12.4]
}

df = pd.DataFrame(data)

# Определите десятилетний тренд минимальных уровней воды.
min_levels_koksu = df['Уровень воды в Koksu River'].min()
min_levels_byzhy = df['Уровень воды в Byzhy River'].min()

trend_koksu = np.polyfit(range(len(df)), df['Уровень воды в Koksu River'], 1)
trend_byzhy = np.polyfit(range(len(df)), df['Уровень воды в Byzhy River'], 1)

# Создайте карту с помощью библиотеки folium.
m = Map(location=[50.0, 70.0], zoom_start=6)

Marker(location=[50.0, 70.0], popup='Коксу').add_to(m)
Marker(location=[51.0, 71.0], popup='Быжый').add_to(m)

# Добавьте данные о уровнях воды на карту.
for i in range(len(df)):
    Marker(location=[50.0 + (df['Уровень воды в Koksu River'].iloc[i] - min_levels_koksu) / 10,
                     70.0 + (df['Уровень воды в Byzhy River'].iloc[i] - min_levels_byzhy) / 10],
           popup=f'Дата: {df["Дата"].iloc[i]}, Уровень воды в Koksu River: {df["Уровень воды в Koksu River"].iloc[i]}').add_to(m)

# Сохраните карту.
m.save("208.html")