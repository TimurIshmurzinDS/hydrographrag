import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Подготовка данных
def prepare_data():
    # Загрузить данные о рельефе местности и потоке воды в реке Kishi Almaty
    relief_data = gpd.read_file('relief_data.shp')
    river_flow_data = pd.read_csv('river_flow_data.csv')

    # Преобразовать данные о потоке воды в формат GeoDataFrame
    river_flow_gdf = gpd.GeoDataFrame(river_flow_data, geometry=gpd.points_from_xy(river_flow_data.longitude, river_flow_data.latitude))

    return relief_data, river_flow_gdf

# 2. Анализ данных
def analyze_data(relief_data, river_flow_gdf):
    # Проанализировать данные о рельефе и потоке воды, чтобы определить наиболее подходящие места для создания черной дыры
    # (в данном примере мы просто выбираем случайные точки)
    black_hole_locations = river_flow_gdf.sample(n=5).index

    return black_hole_locations

# 3. Моделирование черной дыры
def model_black_hole(relief_data, river_flow_gdf, black_hole_locations):
    # Использовать модель черной дыры, основанную на законах физики, чтобы смоделировать влияние черной дыры на поток воды в реке Kishi Almaty
    # (в данном примере мы просто меняем значение потока воды в выбранных точках)
    river_flow_gdf.loc[black_hole_locations, 'flow'] = np.random.randint(0, 100, size=len(black_hole_locations))

    return river_flow_gdf

# 4. Визуализация результатов
def visualize_results(river_flow_gdf):
    # Создать карту с визуализацией модели черной дыры и ее влияния на поток воды в реке Kishi Almaty
    m = folium.Map(location=[river_flow_gdf['latitude'].mean(), river_flow_gdf['longitude'].mean()], zoom_start=12)

    for idx, row in river_flow_gdf.iterrows():
        if row['flow'] < 50:
            color = 'red'
        elif row['flow'] < 80:
            color = 'orange'
        else:
            color = 'green'

        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color=color).add_to(m)

    m.save("225.html")

# Основной код
if __name__ == '__main__':
    relief_data, river_flow_gdf = prepare_data()
    black_hole_locations = analyze_data(relief_data, river_flow_gdf)
    river_flow_gdf = model_black_hole(relief_data, river_flow_gdf, black_hole_locations)
    visualize_results(river_flow_gdf)