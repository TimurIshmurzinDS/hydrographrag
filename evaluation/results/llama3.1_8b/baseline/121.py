import pandas as pd
from folium import Map, CircleMarker
import numpy as np

# Загрузим данные о расходе воды для каждой реки за последние 10 лет (предположим, что данные хранятся в файлах csv)
bayankol_data = pd.read_csv('bayankol_water_usage.csv')
shilik_data = pd.read_csv('shilik_water_usage.csv')

# Преобразуем данные в формат, пригодный для анализа
bayankol_data['date'] = pd.to_datetime(bayankol_data['date'])
shilik_data['date'] = pd.to_datetime(shilik_data['date'])

# Рассчитаем средний расход воды для каждой реки за последние 10 лет
bayankol_avg_usage = bayankol_data.groupby('date')['water_usage'].mean().reset_index()
shilik_avg_usage = shilik_data.groupby('date')['water_usage'].mean().reset_index()

# Сравним средние расходы воды для двух рек
avg_usage_comparison = pd.merge(bayankol_avg_usage, shilik_avg_usage, on='date', suffixes=('_bayankol', '_shilik'))

# Визуализируем результат на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in avg_usage_comparison.iterrows():
    if row['water_usage_bayankol'] > row['water_usage_shilik']:
        color = 'red'
    else:
        color = 'green'
    CircleMarker([row['date'].timetuple().tm_yday / 365 * 180 + 90, np.radians(row['water_usage_bayankol'])], radius=5, color=color).add_to(m)

m.save("121.html")