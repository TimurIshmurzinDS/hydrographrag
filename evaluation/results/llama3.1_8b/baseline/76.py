import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузим данные о гидропостах и реке из соответствующих источников.
hydroposts_data = pd.read_csv('hydroposts.csv')
river_data = pd.read_csv('river.csv')

# Создадим географическую модель, включающую реку и гидропосты.
m = Map(location=[55.0, 60.0], zoom_start=6)

# Добавим гидропосты на карту.
for index, row in hydroposts_data.iterrows():
    Marker(
        location=[row['latitude'], row['longitude']],
        popup=f'Гидропост {row["name"]}: текущий расход воды - {row["water_flow"]} м³/с',
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Оценим риск паводка на основе текущего расхода воды в каждом гидропосте.
hydroposts_data['risk'] = hydroposts_data['water_flow'].apply(lambda x: 'высокий' if x > 1000 else 'низкий')

# Добавим риски паводков на карту.
for index, row in hydroposts_data.iterrows():
    Marker(
        location=[row['latitude'], row['longitude']],
        popup=f'Риск паводка: {row["risk"]}',
        icon=folium.Icon(color='red' if row['risk'] == 'высокий' else 'green')
    ).add_to(m)

# Визуализируем результаты на карте.
m.save("76.html")