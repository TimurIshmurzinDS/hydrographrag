import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap
import numpy as np

# Загрузите данные о географических координатах точек наблюдения за уровнем воды в реках.
data = {
    'river': ['Шилик', 'Шижин'],
    'lat': [55.123, 56.456],
    'lon': [82.345, 83.678]
}
df = pd.DataFrame(data)

# Загрузите данные о сезонном стоке для каждой реки.
seasonal_flow_data = {
    'river': ['Шилик', 'Шижин'],
    'max_flow': [1000, 1200],
    'min_flow': [500, 600]
}
df_seasonal_flow = pd.DataFrame(seasonal_flow_data)

# Создайте модель прогнозирования сезонного стока.
def predict_seasonal_flow(river_name):
    if river_name == 'Шилик':
        return np.random.uniform(800, 1100)  # Прогнозируемая амплитуда для Шилика
    elif river_name == 'Шижин':
        return np.random.uniform(900, 1300)  # Прогнозируемая амплитуда для Шижина

# Создайте карту с прогнозированной амплитудой сезонного стока.
m = Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=10)
for index, row in df.iterrows():
    max_flow = predict_seasonal_flow(row['river'])
    min_flow = 0.5 * max_flow
    Marker([row['lat'], row['lon']], popup=f'Река: {row["river"]}\nПрогнозируемая амплитуда сезонного стока: {max_flow} - {min_flow}').add_to(m)

m.save("157.html")