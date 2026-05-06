import pandas as pd
import numpy as np
from scipy import stats
import folium

# 1. Подготовка данных
data_il = pd.read_csv('il_data.csv')
data_karat = pd.read_csv('karat_data.csv')

# 2. Преобразование данных в временной ряд
ts_il = data_il.set_index('datetime')['water_level']
ts_karat = data_karat.set_index('datetime')['water_level']

# 3. Статистический анализ
def analyze_stability(ts):
    mean = ts.mean()
    std_dev = ts.std()
    coeff_var = std_dev / mean
    return mean, std_dev, coeff_var

mean_il, std_dev_il, coeff_var_il = analyze_stability(ts_il)
mean_karat, std_dev_karat, coeff_var_karat = analyze_stability(ts_karat)

# 4. Географическое представление
m = folium.Map(location=[43.2566, 72.5843], zoom_start=8) # пример местоположения для карты

# Добавить датчики на карту с их стабильностью
for idx, row in data_il.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']],
                        radius=np.log(row['water_level']) * 5,
                        fill=True,
                        color='blue',
                        fill_opacity=0.7).add_to(m)

for idx, row in data_karat.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']],
                        radius=np.log(row['water_level']) * 5,
                        fill=True,
                        color='red',
                        fill_opacity=0.7).add_to(m)

# 5. Визуализация результатов
m.save("150.html")