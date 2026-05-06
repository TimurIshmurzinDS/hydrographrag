import pandas as pd
from folium import Map, Marker, CircleMarker
import numpy as np

# Сбор данных о уровнях воды в реке за период весеннего паводка (предположим, данные хранятся в файле 'water_levels.csv')
data = pd.read_csv('water_levels.csv')

# Анализ данных для определения даты и времени, когда уровень воды был наибольшим
max_level_date = data['date'].loc[data['level'].idxmax()]
max_level_time = data['time'].loc[data['level'].idxmax()]

# Использование геообработки для создания карты с указанием зоны затопления и пикового уровня воды
m = Map(location=[43.65, 79.85], zoom_start=10)

# Добавление маркера на карте с указанием пикового уровня воды
Marker([43.65, 79.85], popup=f'Пиковый уровень воды: {data["level"].max()} м').add_to(m)

# Добавление круга на карте с указанием зоны затопления
CircleMarker([43.65, 79.85], radius=10000, color='red', fill=True).add_to(m)

# Сохранение карты в файл '22.html'
m.save("22.html")