import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np

# Пример данных (замените на реальные данные)
data = {
    'latitude': [40.123, 40.456],  # Широты для Aksu и Temirlik рек
    'longitude': [74.987, 75.123],  # Долготы для Aksu и Temirlik рек
    'elevation': [1000, 1200],      # Высота над уровнем моря
    'precipitation': [500, 400]     # Годовой осадок (мм)
}

df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[np.mean(df['latitude']), np.mean(df['longitude'])], zoom_start=10)

# Добавление слоя тепловых точек для визуализации риска засухи
heat_data = [[row['latitude'], row['longitude'], row['precipitation']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("111.html")

print("Карта сохранена как 111.html")