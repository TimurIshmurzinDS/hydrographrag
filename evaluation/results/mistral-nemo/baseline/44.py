import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузить данные о качестве воды реки Шынжалы из CSV файла
data = pd.read_csv('shynjaly_water_quality.csv')

# Создать GeoDataFrame из данных о качестве воды
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Визуализировать данные на карте с помощью Folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Определить цвета для маркеров в зависимости от показателя качества воды
colors = {
    'good': '#00ff00',  # Зеленый - хорошее качество
    'fair': '#ffff00',  # Желтый - среднее качество
    'poor': '#ff0000'   # Красный - плохое качество
}

# Добавить маркеры на карту в соответствии с показателями качества воды
for index, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Качество воды: {row['water_quality']}", icon=folium.Icon(color=colors[row['water_quality']])).add_to(m)

# Сохранить карту как HTML-файл
m.save("44.html")