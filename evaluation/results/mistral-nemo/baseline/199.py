import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import folium

# 1. Подготовка данных
data_rainfall = pd.read_csv('historical_rainfall.csv')
data_discharge_urzhar = pd.read_csv('discharge_urzhar.csv')
data_discharge_byzhy = pd.read_csv('discharge_byzhy.csv')

# 2. Преобразование данных
data_rainfall['year'] = pd.DatetimeIndex(data_rainfall['date']).year
data_rainfall_monthly = data_rainfall.groupby(['year', pd.Grouper(key='date', freq='M')]).mean().reset_index()
data_discharge_urzhar['year'] = pd.DatetimeIndex(data_discharge_urzhar['date']).year
data_discharge_byzhy['year'] = pd.DatetimeIndex(data_discharge_byzhy['date']).year

# 3. Вычисление корреляции
corr_urzhar, _ = pearsonr(data_rainfall_monthly['rainfall'], data_discharge_urzhar['discharge'])
corr_byzhy, _ = pearsonr(data_rainfall_monthly['rainfall'], data_discharge_byzhy['discharge'])

# 4. Визуализация результатов
m = folium.Map(location=[53.2190, 68.9719], zoom_start=8) # примерные координаты для карты

folium.Marker([data_rainfall_monthly['lat'].mean(), data_rainfall_monthly['lon'].mean()],
              popup=f'Корреляция с рекой Urzhar: {corr_urzhar:.2f}\n'
                    f'Корреляция с рекой Byzhy: {corr_byzhy:.2f}').add_to(m)

m.save("199.html")