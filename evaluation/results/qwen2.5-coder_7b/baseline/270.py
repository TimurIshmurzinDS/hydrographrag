import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных о уровне воды в реке Талгар (в метрах)
water_level_data = {
    'latitude': [51.23, 51.24, 51.25],
    'longitude': [76.45, 76.46, 76.47],
    'level': [0.5, 0.8, 1.2]
}

# Пример данных о зеленом и красном каналах спутниковых изображений
satellite_data = {
    'latitude': [51.23, 51.24, 51.25],
    'longitude': [76.45, 76.46, 76.47],
    'green_channel': [0.3, 0.4, 0.5],
    'red_channel': [0.1, 0.2, 0.3]
}

# Преобразование данных в DataFrame
water_level_df = pd.DataFrame(water_level_data)
satellite_df = pd.DataFrame(satellite_data)

# Обработка данных (пример: удаление пропущенных значений)
water_level_df.dropna(inplace=True)
satellite_df.dropna(inplace=True)

# Вычисление NDVI
satellite_df['ndvi'] = (satellite_df['green_channel'] - satellite_df['red_channel']) / \
                       (satellite_df['green_channel'] + satellite_df['red_channel'])

# Определение порога уровня воды (например, 1.0 метр)
water_level_threshold = 1.0

# Создание карты
m = folium.Map(location=[51.24, 76.46], zoom_start=13)

# Добавление слоя NDVI на карту
ndvi_data = [[row['latitude'], row['longitude'], row['ndvi']] for index, row in satellite_df.iterrows()]
HeatMap(ndvi_data).add_to(m)

# Добавление слоя уровней воды на карту
water_level_data = [[row['latitude'], row['longitude'], row['level']] for index, row in water_level_df.iterrows()]
folium.plugins.HeatMap(water_level_data, radius=25).add_to(m)

# Сохранение карты
m.save("270.html")