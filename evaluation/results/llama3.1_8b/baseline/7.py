import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор данных о текущем уровне воды в реке Батареки (для примера используется фиксированные данные)
data = {
    'Latitude': [48.65, 48.68, 48.72],
    'Longitude': [39.32, 39.35, 39.38],
    'Water Level': [1.2, 1.5, 1.8]
}

df = pd.DataFrame(data)

# Подготовка и очистка данных
# Для примера данные уже очищены

# Анализ данных (для примера используется статистический анализ)
print(df.describe())

# Визуализация результатов на карте
m = Map(location=[48.67, 39.35], zoom_start=12)

for index, row in df.iterrows():
    Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f'Уровень воды: {row["Water Level"]} м',
        icon=None
    ).add_to(m)

HeatMap(data=df[['Latitude', 'Longitude']].values, radius=10).add_to(m)

m.save("7.html")