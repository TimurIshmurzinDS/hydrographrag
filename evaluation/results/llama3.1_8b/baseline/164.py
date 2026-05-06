import pandas as pd
from folium import Map, Marker
import numpy as np

# Сбор данных о реках и их гидрологических характеристиках
data = {
    'river': ['Ili River', 'Shynzhaly River'],
    'length': [1000, 500],
    'width': [10, 5],
    'slope': [0.01, 0.02]
}

df = pd.DataFrame(data)

# Создание модели динамики водного потока
def water_flow_model(river_length, river_width, slope):
    return (river_length * river_width * slope) / 100

# Анализ исторических данных о паводках и определение закономерностей
historical_data = {
    'year': [2010, 2015, 2020],
    'pavodk_level': [10, 15, 20]
}

df_historical = pd.DataFrame(historical_data)

# Создание модели вероятности экстремальных паводков
def extreme_pavodk_model(pavodk_level):
    return (pavodk_level / 100) * np.random.uniform(0.8, 1.2)

# Визуализация результатов на карте
m = Map(location=[46.5, 68], zoom_start=6)
for index, row in df.iterrows():
    marker = Marker([row['length'], row['width']], popup=f"Река: {row['river']}")
    m.add_child(marker)

# Рассчет вероятности экстремальных паводков
df['extreme_pavodk_probability'] = df.apply(lambda x: extreme_pavodk_model(water_flow_model(x['length'], x['width'], x['slope']) * 10), axis=1)

# Визуализация результатов на карте с учетом вероятности экстремальных паводков
for index, row in df.iterrows():
    marker = Marker([row['length'], row['width']], popup=f"Река: {row['river']}, Вероятность экстремального паводка: {row['extreme_pavodk_probability']:.2f}")
    m.add_child(marker)

# Сохранение карты в файл
m.save("164.html")