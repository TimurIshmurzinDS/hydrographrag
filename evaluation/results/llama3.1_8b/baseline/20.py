import pandas as pd
import numpy as np
from folium import Map, CircleMarker
import matplotlib.pyplot as plt

# Сбор и преобразование данных
data = {
    'Дата': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Расход воды (м³/с)': [100, 120, 150],
    'Уровень воды (м)': [5, 6, 7]
}

df = pd.DataFrame(data)

# Анализ данных
max_flow = df['Расход воды (м³/с)'].max()
min_flow = df['Расход воды (м³/с)'].min()

print(f'Максимальный расход воды: {max_flow} м³/с')
print(f'Минимальный расход воды: {min_flow} м³/с')

# Моделирование
def model_flow(date, level):
    # Простая модель: расход воды = 10 * уровень воды + 50
    return 10 * level + 50

df['Прогнозируемый расход'] = df.apply(lambda row: model_flow(row['Дата'], row['Уровень воды (м)']), axis=1)

# Визуализация результатов на карте
m = Map(location=[55.75, 37.62], zoom_start=12)
for index, row in df.iterrows():
    marker = CircleMarker([row['Уровень воды (м)'], row['Расход воды (м³/с)']], radius=row['Прогнозируемый расход'] * 0.1).add_to(m)

m.save("20.html")

# Визуализация результатов в виде графика
plt.plot(df['Дата'], df['Расход воды (м³/с)'], label='Фактический расход')
plt.plot(df['Дата'], df['Прогнозируемый расход'], label='Прогнозируемый расход')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м³/с)')
plt.legend()
plt.show()