import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные в формате CSV с колонками: 'date', 'latitude', 'longitude', 'pollutant_concentration'
# Для примера создадим фейковые данные
np.random.seed(0)
dates = pd.date_range(start='2018-01-01', end='2023-01-01', freq='D')
latitudes = np.random.uniform(low=29.5, high=30.5, size=len(dates))
longitudes = np.random.uniform(low=-116.5, high=-115.5, size=len(dates))
pollutant_concentration = np.random.normal(loc=10, scale=2, size=len(dates))

data = pd.DataFrame({
    'date': dates,
    'latitude': latitudes,
    'longitude': longitudes,
    'pollutant_concentration': pollutant_concentration
})

# Преобразуем данные для визуализации на карте
heat_data = data[['latitude', 'longitude', 'pollutant_concentration']].values.tolist()

# Создание карты с использованием folium
m = folium.Map(location=[30.0, -116.0], zoom_start=9)

# Добавление тепловой карты на основании данных о загрязнении
HeatMap(heat_data).add_to(m)

# Сохранение карты в файл
m.save("56.html")