import pandas as pd
import numpy as np
from scipy import stats
import folium

# 1. Подготовьте данные
data = pd.read_csv('historical_water_levels.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 2. Выберите порог паводка
flood_threshold = 50

# 3. Расчет вероятности превышения порога
def calculate_flood_probability(series):
    flood_events = series[series > flood_threshold]
    if len(flood_events) == 0:
        return 0
    else:
        return len(flood_events) / len(series)

data['flood_probability'] = data['water_level'].apply(calculate_flood_probability)

# 4. Визуализация результатов
m = folium.Map(location=[43.25, 72.6], zoom_start=10)

for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=np.log(row['flood_probability'] + 1) * 5,
        color='blue',
        fill=True
    ).add_to(m)

m.save("203.html")