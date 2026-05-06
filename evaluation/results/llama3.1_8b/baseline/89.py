import pandas as pd
import numpy as np
from folium import Map, CircleMarker

# Загрузите данные о расходе и уровне воды для рек Баскан и Прохождение.
baskan_flow = pd.read_csv('baskan_flow.csv')
prokhodnaya_level = pd.read_csv('prokhodnaya_level.csv')

# Рассчитайте среднее значение расхода и уровня воды для каждого месяца в течение 10 лет.
baskan_avg_flow = baskan_flow.groupby(pd.Grouper(key='date', freq='M'))['flow'].mean()
prokhodnaya_avg_level = prokhodnaya_level.groupby(pd.Grouper(key='date', freq='M'))['level'].mean()

# Найдите разницу между средним расходом на реке Баскан и средним уровнем на реке Прохождение.
diff = baskan_avg_flow - prokhodnaya_avg_level

# Создайте карту с использованием библиотеки Folium.
m = Map(location=[55.0, 37.5], zoom_start=6)

# Добавьте маркеры для каждого месяца в течение 10 лет.
for i in range(120):
    date = pd.to_datetime('2020-01-01') + pd.DateOffset(months=i)
    flow = baskan_avg_flow.iloc[i]
    level = prokhodnaya_avg_level.iloc[i]
    diff_val = diff.iloc[i]
    
    # Если разница больше 10, добавьте красный маркер.
    if diff_val > 10:
        color = 'red'
    else:
        color = 'blue'
        
    CircleMarker(location=[55.0 + np.random.uniform(-1, 1), 37.5 + np.random.uniform(-1, 1)], radius=2,
                 color=color).add_to(m)

# Сохраните карту в файл.
m.save("89.html")