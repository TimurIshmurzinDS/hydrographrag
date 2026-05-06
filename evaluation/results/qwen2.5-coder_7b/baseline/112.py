import folium
from shapely.geometry import Point, LineString
import pandas as pd

# Пример данных о реках и их водопотреблении
data = {
    'river_name': ['Kurty River', 'Urzhar River', 'Byzhy River'],
    'latitude': [50.1234, 51.5678, 52.9012],
    'longitude': [30.1234, 31.5678, 32.9012],
    'water_consumption': [1000, 1500, 2000]  # в кубических метрах в год
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Создаем карту
m = folium.Map(location=[51.5678, 31.5678], zoom_start=6)

# Добавляем маркеры для каждой реки с уровнем водопотребления
for index, row in df.iterrows():
    location = (row['latitude'], row['longitude'])
    folium.Marker(location, popup=f"{row['river_name']}<br>Водопотребление: {row['water_consumption']} куб.м/год").add_to(m)

# Сохраняем карту
m.save("112.html")

print("Карта сохранена как 112.html")