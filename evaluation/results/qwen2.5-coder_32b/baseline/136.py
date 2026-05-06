import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть DataFrame с данными о датчиках
data = {
    'id': [1, 2, 3, 4],
    'latitude': [56.0089, 56.0100, 56.0110, 56.0120],
    'longitude': [92.8796, 92.8800, 92.8805, 92.8810],
    'status': ['активен', 'неактивен', 'исправен', 'неисправен']
}

# Шаг 2: Подготовка данных
df = pd.DataFrame(data)
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Шаг 3: Анализ данных (в данном случае статус уже включен в данные)
# Можно добавить дополнительную логику для анализа, если необходимо

# Шаг 4: Визуализация данных
m = folium.Map(location=[56.0100, 92.8800], zoom_start=13)

# Добавление маркеров на карту
for _, row in gdf.iterrows():
    popup_text = f"ID: {row['id']}\nСтатус: {row['status']}"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color='green' if row['status'] in ['активен', 'исправен'] else 'red')
    ).add_to(m)

# Шаг 5: Сохранение результата
m.save("136.html")