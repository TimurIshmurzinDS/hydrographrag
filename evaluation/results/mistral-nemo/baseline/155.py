import pandas as pd
import numpy as np
from datetime import datetime
import folium

# Загрузка данных о уровнях воды для рек Bayankol River и Lepsy River
bayankol_data = pd.read_csv('bayankol_river_water_levels.csv')
lepsy_data = pd.read_csv('lepsy_river_water_levels.csv')

# Преобразование дат в формат datetime
bayankol_data['date'] = pd.to_datetime(bayankol_data['date'])
lespy_data['date'] = pd.to_datetime(lepsy_data['date'])

# Вычисление среднего уровня воды за каждый месяц весны для Bayankol River
bayankol_spring_levels = bayankol_data.groupby([pd.Grouper(key='date', freq='M'), 'month'])['water_level'].mean()

# Вычисление среднего уровня воды за каждый месяц весны для Lepsy River
lepsy_spring_levels = lepsy_data.groupby([pd.Grouper(key='date', freq='M'), 'month'])['water_level'].mean()

# Построение графика изменения среднего уровня воды для каждого месяца весны в течение нескольких лет

# Визуализация результатов на карте с помощью библиотеки folium
m = folium.Map(location=[bayankol_data['latitude'].mean(), bayankol_data['longitude'].mean()], zoom_start=8)

# Отображение средних уровней воды за каждый месяц весны для Bayankol River на карте
for idx, row in bayankol_spring_levels.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=np.abs(row['water_level']) / 10,
                        color='blue',
                        fill=True).add_to(m)

# Отображение средних уровней воды за каждый месяц весны для Lepsy River на карте
for idx, row in lepsy_spring_levels.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=np.abs(row['water_level']) / 10,
                        color='red',
                        fill=True).add_to(m)

# Сохранение финальной карты как "155.html"
m.save("155.html")