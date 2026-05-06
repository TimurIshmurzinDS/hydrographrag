import pandas as pd
import folium
from folium.plugins import HeatMap

# Загрузка данных
data = pd.read_csv('karatal_water_flow.csv')

# Предположим, что данные имеют следующие столбцы: 'latitude', 'longitude', 'flow_rate'
# Пример данных:
# latitude,longitude,flow_rate
# 40.7128,-74.0060,500
# 40.7130,-74.0062,550
# ...

# Анализ данных
mean_flow = data['flow_rate'].mean()
max_flow = data['flow_rate'].max()
min_flow = data['flow_rate'].min()

print(f"Средний расход воды: {mean_flow}")
print(f"Максимальный расход воды: {max_flow}")
print(f"Минимальный расход воды: {min_flow}")

# Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление теплового картографа
heat_data = [[row['latitude'], row['longitude'], row['flow_rate']] for index, row in data.iterrows()]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("214.html")