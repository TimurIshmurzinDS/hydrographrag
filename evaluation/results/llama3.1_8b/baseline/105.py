import pandas as pd
from folium import Map, Marker

# Загрузите данные о реках и их координатах (предположим, что они хранятся в файле rivers.csv)
rivers_data = pd.read_csv('rivers.csv')

# Сгруппируйте реки по регионам на основе их координат
grouped_rivers = rivers_data.groupby(['region', 'river_name'])

# Найдите реки, чьи координаты находятся в одном регионе
single_region_rivers = []
for name, group in grouped_rivers:
    if len(group['coordinates'].unique()) == 1:  # Если у реки есть только одна координата
        single_region_rivers.append((name[0], name[1]))

# Создайте карту с маркерами для каждой реки из списка
m = Map(location=[43.25, 76.9], zoom_start=10)
for river in single_region_rivers:
    coordinates = rivers_data[(rivers_data['region'] == river[0]) & (rivers_data['river_name'] == river[1])]['coordinates'].iloc[0]
    Marker(location=coordinates, popup=f'{river[1]} в регионе {river[0]}').add_to(m)

# Сохраните карту как HTML-файл
m.save("105.html")