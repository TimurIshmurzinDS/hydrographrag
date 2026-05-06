import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# 1. Загрузка данных о уровнях воды (замените на актуальный источник)
data = pd.read_csv("water_levels_osek_river.csv")

# 2. Создание слоя точек с уровнями воды
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# 3. Интерполяция для создания модели поверхности (требуется библиотека, например, scipy)
# ...

# 4. Визуализация на карте folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление слоя с уровнями воды
folium.GeoJson(gdf).add_to(m)

# ... (Добавление цветовой шкалы и других элементов визуализации)

m.save("26.html")