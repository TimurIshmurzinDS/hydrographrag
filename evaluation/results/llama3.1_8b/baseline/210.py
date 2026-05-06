import pandas as pd
import numpy as np
from folium import Map, CircleMarker
import matplotlib.pyplot as plt

# Загрузим исторические данные о стоке рек из соответствующих источников.
# Для примера мы будем использовать фиктивные данные.
data_lepsy = {
    'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01',
             '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01',
             '2022-11-01', '2022-12-01'],
    'flow': [100, 120, 150, 180, 200, 220, 250, 280, 300, 320, 350, 380]
}
data_aksu = {
    'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01',
             '2022-06-01', '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01',
             '2022-11-01', '2022-12-01'],
    'flow': [80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]
}

df_lepsy = pd.DataFrame(data_lepsy)
df_aksu = pd.DataFrame(data_aksu)

# Преобразуем данные в единообразный формат для анализа.
df_lepsy['date'] = pd.to_datetime(df_lepsy['date'])
df_aksu['date'] = pd.to_datetime(df_aksu['date'])

# Разделим данные на сезонные периоды (весну, лето, осень и зиму).
seasons = ['winter', 'spring', 'summer', 'autumn']
df_lepsy['season'] = np.select([df_lepsy['date'].dt.month < 3, df_lepsy['date'].dt.month < 6,
                                df_lepsy['date'].dt.month < 9, True], [0, 1, 2, 3])
df_aksu['season'] = np.select([df_aksu['date'].dt.month < 3, df_aksu['date'].dt.month < 6,
                               df_aksu['date'].dt.month < 9, True], [0, 1, 2, 3])

# Оценим средний сток каждой реки по сезонам.
mean_flow_lepsy = df_lepsy.groupby('season')['flow'].mean()
mean_flow_aksu = df_aksu.groupby('season')['flow'].mean()

# Сравним результаты между двумя реками.
print("Средний сток Лепсы:")
print(mean_flow_lepsy)
print("\nСредний сток Аксу:")
print(mean_flow_aksu)

# Визуализируем результаты на карте с помощью библиотеки Folium.
m = Map(location=[50.0, 70.0], zoom_start=4)
for i in range(4):
    lat_lepsy = np.random.uniform(40, 60)
    lon_lepsy = np.random.uniform(60, 80)
    lat_aksu = np.random.uniform(40, 60)
    lon_aksu = np.random.uniform(60, 80)
    CircleMarker([lat_lepsy, lon_lepsy], radius=10).add_to(m)
    CircleMarker([lat_aksu, lon_aksu], radius=10).add_to(m)

m.save("210.html")