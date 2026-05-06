import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор и очистка данных о расходе воды в реке Кумбель.
data = {
    'location': ['Кумбель', 'Кумбель', 'Кумбель'],
    'water_usage': [1000, 2000, 3000],
    'x': [-35.5, -36.2, -37.1],  # Координаты на карте
    'y': [150.8, 151.3, 152.4]   # Координаты на карте
}

df = pd.DataFrame(data)

# Геопозиционирование точек сбора воды.
m = Map(location=[-36.5, 151.5], zoom_start=10)
for index, row in df.iterrows():
    Marker([row['y'], row['x']], popup=f'Расход воды: {row["water_usage"]} м³').add_to(m)

# Визуализация результатов на карте.
HeatMap(data=df[['x', 'y']].values, radius=10).add_to(m)
m.save("37.html")