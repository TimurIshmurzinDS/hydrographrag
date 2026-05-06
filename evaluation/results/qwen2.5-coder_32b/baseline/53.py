import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные в формате CSV с колонками: 'date', 'temperature', 'latitude', 'longitude'
# Загрузка данных за 2021 и 2022 годы
data_2021 = pd.read_csv('shilik_river_temperature_2021.csv')
data_2022 = pd.read_csv('shilik_river_temperature_2022.csv')

# Обработка данных: преобразование даты и фильтрация по нужным столбцам
data_2021['date'] = pd.to_datetime(data_2021['date'])
data_2022['date'] = pd.to_datetime(data_2022['date'])

# Формирование данных для тепловой карты (средняя температура за каждый день)
heatmap_data_2021 = data_2021.groupby(['latitude', 'longitude']).mean().reset_index()
heatmap_data_2022 = data_2022.groupby(['latitude', 'longitude']).mean().reset_index()

# Создание базовой карты
m = folium.Map(location=[54.9386, 73.3961], zoom_start=10)  # Координаты примерно по центру реки Шилик

# Добавление тепловой карты для 2021 года
heat_data_2021 = [[row['latitude'], row['longitude'], row['temperature']] for index, row in heatmap_data_2021.iterrows()]
HeatMap(heat_data_2021, name='Температура воды в 2021 году').add_to(m)

# Добавление тепловой карты для 2022 года
heat_data_2022 = [[row['latitude'], row['longitude'], row['temperature']] for index, row in heatmap_data_2022.iterrows()]
HeatMap(heat_data_2022, name='Температура воды в 2022 году').add_to(m)

# Добавление слоев управления
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("53.html")