import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные в формате CSV с колонками: 'river', 'latitude', 'longitude', 'pollution_level'
data = {
    'river': ['Byzhy River'] * 10 + ['Tekeli River'] * 10,
    'latitude': np.random.uniform(42.5, 43.5, 20),
    'longitude': np.random.uniform(69.0, 70.0, 20),
    'pollution_level': np.random.randint(1, 10, 20)  # Уровень загрязнения от 1 до 9
}

df = pd.DataFrame(data)

# Анализ данных: вычисление среднего уровня загрязнения для каждой реки
average_pollution = df.groupby('river')['pollution_level'].mean().reset_index()
print(average_pollution)

# Создание карты с использованием folium
m = folium.Map(location=[43.0, 69.5], zoom_start=8)

# Добавление тепловой карты для уровня загрязнения
heat_data = df[['latitude', 'longitude', 'pollution_level']].values.tolist()
HeatMap(heat_data).add_to(m)

# Добавление маркеров с информацией о среднем уровне загрязнения
for index, row in average_pollution.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Средний уровень загрязнения: {row['pollution_level']}",
        icon=folium.Icon(color='red' if row['river'] == 'Byzhy River' else 'blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("119.html")