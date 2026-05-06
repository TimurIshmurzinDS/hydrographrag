import folium
from folium.plugins import HeatMap
import pandas as pd

# Данные о реке Кишинь-Алматы (предположительно)
data = {
    'широта': [43.123, 43.456],
    'долгота': [76.789, 77.012],
    'высота_водопада': [10, 20],
    'площадь_бассейна': [100, 200],
    'скорость_течения': [1, 2]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Создаем карту с помощью Folium
m = folium.Map(location=[43.5, 76.75], zoom_start=12)

# Добавляем слой для визуализации потока воды
folium.plugins.HeatMap(
    data=df[['широта', 'долгота']].values,
    radius=10,
    blur=1,
    max_val=2,
).add_to(m)

# Добавляем слой для визуализации черной дыры
folium.Marker(
    location=[43.5, 76.75],
    popup='Черная дыра',
    icon=folium.Icon(color='black')
).add_to(m)

# Сохраняем карту в файл
m.save("225.html")