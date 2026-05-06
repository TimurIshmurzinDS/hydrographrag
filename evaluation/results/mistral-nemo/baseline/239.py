import folium
import pandas as pd

# Загружаем данные о уровне реки Коктал и их геолокацию
data = pd.read_csv('koktal_water_level.csv')

# Создаем карту с центром на местоположении реки Коктал
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Визуализируем уровень реки Коктал на карте, используя цвета для обозначения различных уровней воды
for index, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['water_level']/10,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# Сохраняем финальную карту как "239.html"
m.save("239.html")