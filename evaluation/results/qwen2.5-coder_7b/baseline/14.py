import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'latitude': [52.123, 52.124, 52.125],
    'longitude': [70.123, 70.124, 70.125],
    'temperature': [18, 19, 20],
    'pH': [6.8, 6.9, 7.0]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[52.124, 70.124], zoom_start=13)

# Добавление маркеров с параметрами качества воды
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура: {row['temperature']}°C<br>pH: {row['pH']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Добавление теплового карты (если есть данные о плотности точек)
if len(df) > 1:
    heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("14.html")