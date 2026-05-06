import pandas as pd
import numpy as np
from folium import Map, Marker, CircleMarker, Polygon, PolyLine
from folium.plugins import HeatMap

# Текущее состояние реки Шарын (предположительно)
data = {
    'Latitude': [48.5, 49.2, 50.1],
    'Longitude': [87.3, 88.1, 89.2],
    'Flow': [100, 120, 150]
}

df = pd.DataFrame(data)

# Моделирование изменений в гидрологическом режиме
np.random.seed(0)
data_change = {
    'Latitude': np.random.uniform(48.4, 50.6, size=10),
    'Longitude': np.random.uniform(87.2, 90.2, size=10),
    'Flow': np.random.uniform(80, 180, size=10)
}

df_change = pd.DataFrame(data_change)

# Анализ влияния на экотуризм
def calculate_ecotourism(df):
    # Предположим, что доступность и безопасность зависят от потока воды
    accessibility = df['Flow'] / 100
    safety = np.where(df['Flow'] > 120, 1, 0)
    
    return accessibility * safety

df_change['Ecotourism'] = calculate_ecotourism(df_change)

# Визуализация результатов
m = Map(location=[49.3, 88.7], zoom_start=8)

for i in range(len(df)):
    Marker([df.iloc[i]['Latitude'], df.iloc[i]['Longitude']], popup='Текущее состояние').add_to(m)
    
for i in range(len(df_change)):
    CircleMarker([df_change.iloc[i]['Latitude'], df_change.iloc[i]['Longitude']], radius=df_change.iloc[i]['Flow'] / 10, color='red', fill=True).add_to(m)

HeatMap(data=list(zip(df_change['Latitude'], df_change['Longitude'])), min_opacity=0.5, max_val=180, radius=20).add_to(m)

m.save("194.html")