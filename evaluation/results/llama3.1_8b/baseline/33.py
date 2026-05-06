import pandas as pd
from folium import Map, Marker

# Сбор данных (предположим, что у нас есть таблица с данными)
data = {
    'координаты': [(45.1234, 55.6789), (46.2345, 56.7890)],
    'объем_воды': [100, 200]
}

df = pd.DataFrame(data)

# Геопространственное моделирование
def calculate_water_usage(lat, lon):
    # Предположим, что у нас есть функция, которая может прогнозировать объем воды на основе координат
    return df.loc[(df['координаты'] == (lat, lon)), 'объем_воды'].values[0]

# Анализ данных и определение областей с высоким потреблением воды
high_water_usage_areas = []
for index, row in df.iterrows():
    water_usage = calculate_water_usage(row['координаты'][0], row['координаты'][1])
    if water_usage > 150:
        high_water_usage_areas.append((row['координаты'], water_usage))

# Визуализация результатов на карте
m = Map(location=[45.1234, 55.6789], zoom_start=10)
for area in high_water_usage_areas:
    Marker(area[0]).add_to(m)

m.save("33.html")