import folium
from folium.plugins import HeatMap
import pandas as pd

# Загрузите данные о гидропостах и уровнях воды в DataFrames
hydro_posts = pd.DataFrame({
    'id': [1, 2, 3],
    'x': [-30.0, -20.0, -10.0],  # координаты x
    'y': [40.0, 50.0, 60.0]  # координаты y
})

water_levels = pd.DataFrame({
    'id': [1, 2, 3],
    'x': [-30.0, -20.0, -10.0],  # координаты x
    'y': [40.0, 50.0, 60.0],  # координаты y
    'level': [5.0, 6.0, 7.0]  # текущие уровни воды
})

# Создайте карту с помощью Folium
m = folium.Map(location=[45.0, -15.0], zoom_start=10)

# Добавьте слой гидропостов на карту
folium.Marker(
    location=[hydro_posts['y'].iloc[0], hydro_posts['x'].iloc[0]],
    popup='Гидропост 1',
).add_to(m)

for i in range(len(hydro_posts)):
    folium.Marker(
        location=[hydro_posts['y'].iloc[i], hydro_posts['x'].iloc[i]],
        popup=f'Гидропост {i+1}',
    ).add_to(m)

# Добавьте слой уровней воды на карту
heat_map = HeatMap(
    data=water_levels[['x', 'y', 'level']].values,
    radius=10,
).add_to(m)

# Сохраните карту в файл
m.save("63.html")