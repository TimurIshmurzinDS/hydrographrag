import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
import folium

# 1. Подготовка данных
def load_data(file_path):
    return gpd.read_file(file_path)

# 2. Вычисление параметров дренажной сети
def calculate_density(drainage_network):
    # Рассчитать плотность дренажной сети на основе количества водотоков в каждом участке бассейна реки Текес
    drainage_density = len(drainage_network) / np.size(drainage_network)
    return drainage_density

# 3. Учёт топологических особенностей
def calculate_topological_features(river_network):
    # Использовать модель гидрографической сети для учёта топологических особенностей реки Текес и её притоков
    topological_features = river_network.length / river_network.area
    return topological_features

# 4. Визуализация результатов
def visualize_results(drainage_density, topological_features):
    # Отобразить плотность дренажной сети на карте с использованием библиотеки `folium`
    m = folium.Map(location=[50.7398, 62.417], zoom_start=8)

    for idx, row in drainage_density.iterrows():
        folium.CircleMarker(
            location=(row['y'], row['x']),
            radius=np.log(row['drainage_density'] + 1),
            color='blue',
            fill=True,
            fill_opacity=0.5
        ).add_to(m)

    for idx, row in topological_features.iterrows():
        folium.CircleMarker(
            location=(row['y'], row['x']),
            radius=np.log(row['topological_features'] + 1),
            color='red',
            fill=True,
            fill_opacity=0.5
        ).add_to(m)

    m.save("172.html")

# Загрузка данных о рельефе местности и дренажной сети реки Текес
drainage_network = load_data('drainage_network.shp')
river_network = load_data('river_network.shp')

# Рассчитать плотность дренажной сети на основе количества водотоков в каждом участке бассейна реки Текес
drainage_density = calculate_density(drainage_network)

# Использовать модель гидрографической сети для учёта топологических особенностей реки Текес и её притоков
topological_features = calculate_topological_features(river_network)

# Отобразить плотность дренажной сети на карте с использованием библиотеки `folium`
visualize_results(drainage_density, topological_features)