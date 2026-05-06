import folium
from folium.plugins import HeatMap
import numpy as np

# Загрузка данных о бассейне реки Каскелен (предположим, что данные хранятся в файле 'caskelen.shp')
import geopandas as gpd
gdf = gpd.read_file('caskelen.shp')

# Создание функции для генерации рандомных значений высоты
def generate_heights(gdf):
    # Генерируем рандомные значения высоты на основе данных о бассейне
    heights = np.random.uniform(0, 100, size=(len(gdf),))
    return heights

# Создание функции для визуализации результатов на карте
def visualize_results(gdf, heights):
    # Создаем карту с использованием библиотеки folium
    m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], zoom_start=10)
    
    # Генерируем слой тепловой карты на основе данных о высоте
    heat_data = [[lat, lon, height] for lat, lon, height in zip(gdf.geometry.y, gdf.geometry.x, heights)]
    HeatMap(heat_data, radius=20).add_to(m)
    
    # Сохраняем карту в файл
    m.save("255.html")

# Генерация рандомных значений высоты и визуализация результатов на карте
heights = generate_heights(gdf)
visualize_results(gdf, heights)