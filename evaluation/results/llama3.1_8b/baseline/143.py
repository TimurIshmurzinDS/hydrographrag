import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Шаг 1: Сбор данных о гидропостах
data_karatal = {
    'id': [1, 2, 3],
    'name': ['Гидропост 1', 'Гидропост 2', 'Гидропост 3'],
    'lat': [43.1234, 43.4567, 43.7890],
    'lon': [79.0123, 79.3456, 79.6789],
    'status': ['работает', 'не работает', 'работает']
}

data_lepsa = {
    'id': [1, 2, 3],
    'name': ['Гидропост 1', 'Гидропост 2', 'Гидропост 3'],
    'lat': [43.9012, 44.2345, 44.5678],
    'lon': [80.0123, 80.3456, 80.6789],
    'status': ['не работает', 'работает', 'не работает']
}

df_karatal = pd.DataFrame(data_karatal)
df_lepsa = pd.DataFrame(data_lepsa)

# Шаг 2: Создание географической базы данных
m = Map(location=[43.5, 79.5], zoom_start=10)

# Шаг 3: Анализ состояния работоспособности гидропостов
for i in range(len(df_karatal)):
    if df_karatal.loc[i, 'status'] == 'работает':
        Marker([df_karatal.loc[i, 'lat'], df_karatal.loc[i, 'lon']], popup=df_karatal.loc[i, 'name']).add_to(m)
    else:
        Marker([df_karatal.loc[i, 'lat'], df_karatal.loc[i, 'lon']], popup=df_karatal.loc[i, 'name'], icon=folium.Icon(color='red')).add_to(m)

for i in range(len(df_lepsa)):
    if df_lepsa.loc[i, 'status'] == 'работает':
        Marker([df_lepsa.loc[i, 'lat'], df_lepsa.loc[i, 'lon']], popup=df_lepsa.loc[i, 'name']).add_to(m)
    else:
        Marker([df_lepsa.loc[i, 'lat'], df_lepsa.loc[i, 'lon']], popup=df_lepsa.loc[i, 'name'], icon=folium.Icon(color='red')).add_to(m)

# Шаг 4: Визуализация результатов на карте
m.save("143.html")