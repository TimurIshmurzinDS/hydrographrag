import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': ['2018-01-01', '2018-02-01', '2018-03-01', '2019-01-01', '2019-02-01', '2019-03-01'],
    'river': ['Lepsy', 'Lepsy', 'Lepsy', 'Turgen', 'Turgen', 'Turgen'],
    'water_level': [5.2, 5.4, 5.6, 6.0, 6.2, 6.4]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Группировка по ручью и вычисление среднего уровня воды
trends = df.groupby('river')['water_level'].mean().reset_index()

# Создание карты
m = folium.Map(location=[50.45, 36.92], zoom_start=10)

# Добавление маркеров с трендами уровней воды
for index, row in trends.iterrows():
    folium.Marker(
        location=[50.45, 36.92],  # Здесь нужно указать точные координаты бассейнов
        popup=f"River: {row['river']}, Average Water Level: {row['water_level']:.2f}",
        icon=folium.Icon(color='blue' if row['river'] == 'Lepsy' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("198.html")