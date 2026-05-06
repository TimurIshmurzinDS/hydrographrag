import folium
from folium.plugins import HeatMap
import pandas as pd

# Загрузим данные о реках из источника (в данном случае мы будем использовать фиктивные данные)
data = {
    'river': ['Тентек', 'Шарын'],
    'latitude': [50.123, 52.456],
    'longitude': [70.789, 72.321],
    'status': ['good', 'bad']
}

df = pd.DataFrame(data)

# Создадим географические объекты для каждой реки
m = folium.Map(location=[51.0, 71.5], zoom_start=10)
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}, Статус: {row['status']}",
        icon=folium.Icon(color='green' if row['status'] == 'good' else 'red')
    ).add_to(m)

# Визуализируем результат на карте
m.save("75.html")