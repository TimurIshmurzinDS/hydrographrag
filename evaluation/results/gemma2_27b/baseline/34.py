import folium
import pandas as pd
from shapely.geometry import Point

# Загрузка данных о загрязнении воды (замените на ваш файл)
data = pd.read_csv("pollution_data.csv")

# Создание GeoDataFrame из данных
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Создание карты с folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление точек загрязнения на карту
for index, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='green' if row['pollution_level'] < 5 else 'red', # Пример цветовой шкалы
        popup=f"Pollution Level: {row['pollution_level']}"
    ).add_to(m)

# Добавление слоя реки Лепси (замените на ваш источник данных)
folium.GeoJson("river_lepsi.geojson").add_to(m)

# Сохранение карты
m.save("34.html")