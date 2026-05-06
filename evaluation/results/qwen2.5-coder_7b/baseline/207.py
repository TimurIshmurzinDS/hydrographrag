import pandas as pd
import numpy as np
from scipy.stats import norm, expon
import folium
from folium.plugins import MarkerCluster

# Пример данных (замените на реальные данные)
data_emel = {
    'date': pd.date_range(start='2013-01-01', periods=240, freq='M'),
    'water_level': np.random.normal(loc=50, scale=10, size=240) + np.random.exponential(scale=5, size=240)
}

data_turgen = {
    'date': pd.date_range(start='2013-01-01', periods=240, freq='M'),
    'water_level': np.random.normal(loc=60, scale=15, size=240) + np.random.exponential(scale=7, size=240)
}

df_emel = pd.DataFrame(data_emel)
df_turgen = pd.DataFrame(data_turgen)

# Определение экстремальных значений
def find_extremes(df):
    extremes = []
    for date, level in zip(df['date'], df['water_level']):
        if level > np.percentile(df['water_level'], 95) or level < np.percentile(df['water_level'], 5):
            extremes.append((date, level))
    return pd.DataFrame(extremes, columns=['date', 'extreme_level'])

extremes_emel = find_extremes(df_emel)
extremes_turgen = find_extremes(df_turgen)

# Визуализация на карте
m = folium.Map(location=[50.45, 83.96], zoom_start=10)

marker_cluster_emel = MarkerCluster().add_to(m)
for _, row in extremes_emel.iterrows():
    folium.Marker([row['date'].year, row['extreme_level']], popup=f"Emel River: {row['extreme_level']}", icon=folium.Icon(color='red')).add_to(marker_cluster_emel)

marker_cluster_turgen = MarkerCluster().add_to(m)
for _, row in extremes_turgen.iterrows():
    folium.Marker([row['date'].year, row['extreme_level']], popup=f"Turgen River: {row['extreme_level']}", icon=folium.Icon(color='blue')).add_to(marker_cluster_turgen)

m.save("207.html")