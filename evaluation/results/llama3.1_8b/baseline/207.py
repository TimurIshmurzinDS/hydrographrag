import pandas as pd
import numpy as np
from folium import Map, Marker, CircleMarker
import matplotlib.pyplot as plt

# Загрузка данных о уровнях воды в реках за последние 20 лет (предполагается, что данные хранятся в двух таблицах: emel_river и turgen_river)
emel_data = pd.read_csv('emel_river.csv')
turgen_data = pd.read_csv('turgenev_river.csv')

# Объединение данных о уровнях воды в реках
data = pd.concat([emel_data, turgen_data])

# Определение экстремальных межен как значений, превышающих или равных 90-му процентилю или ниже 10-го процентиля уровней воды
q90 = data['level'].quantile(0.9)
q10 = data['level'].quantile(0.1)

extreme_emel = emel_data[(emel_data['level'] <= q90) | (emel_data['level'] >= q10)]
extreme_turgen = turgen_data[(turgen_data['level'] <= q90) | (turgen_data['level'] >= q10)]

# Подсчет частоты экстремальных межен в каждой реке
freq_emel = extreme_emel.shape[0] / emel_data.shape[0]
freq_turgen = extreme_turgen.shape[0] / turgen_data.shape[0]

print(f'Частота экстремальных межен в реке Эмель: {freq_emel:.2f}')
print(f'Частота экстремальных межен в реке Турген: {freq_turgen:.2f}')

# Сравнение частот экстремальных межен в двух реках
if freq_emel > freq_turgen:
    print('Река Эмель имеет более высокую частоту экстремальных межен.')
elif freq_emel < freq_turgen:
    print('Река Турген имеет более высокую частоту экстремальных межен.')
else:
    print('Частоты экстремальных межен в реках Эмель и Турген равны.')

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
Marker(location=[emel_data['lat'].mean(), emel_data['lon'].mean()], popup='Река Эмель').add_to(m)
CircleMarker(location=[turgen_data['lat'].mean(), turgen_data['lon'].mean()], radius=10000, color='red', fill=True).add_to(m)

# Сохранение карты в файл
m.save("207.html")