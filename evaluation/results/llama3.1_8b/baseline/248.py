import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Данные о реке Аксу (предположим, что они хранятся в DataFrame)
data = {
    'lat': [43.1234, 43.4567, 43.7890],
    'lon': [79.0123, 79.3456, 79.6789]
}
df = pd.DataFrame(data)

# Создаем карту
m = Map(location=[43.5, 79.5], zoom_start=10)

# Добавляем маркеры для реки Аксу на карте
for i in range(len(df)):
    Marker(location=[df['lat'].iloc[i], df['lon'].iloc[i]]).add_to(m)

# Создаем тепловую карту колонизации Марса
heat_data = {
    'lat': [25.0, 35.0, 45.0],
    'lon': [60.0, 70.0, 80.0],
    'value': [10, 20, 30]
}
df_heat = pd.DataFrame(heat_data)
HeatMap(data=df_heat, radius=5).add_to(m)

# Сохраняем карту в файл
m.save("248.html")