import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Подготовка данных о полях, расходе воды и типах культур
fields_data = {
    'id': [1, 2, 3],
    'geometry': [Point(xy) for xy in [(50.7489, 60.6117), (50.7512, 60.6144), (50.7456, 60.6089)]],
    'water_consumption': [1000, 1500, 2000],  # примерные значения расхода воды в м³
    'crop_type': ['пшеница', 'кукуруза', 'овес']  # типы культур
}

# Создание GeoDataFrame для полей
fields_gdf = gpd.GeoDataFrame(fields_data, geometry='geometry')

# 2. Цифровая модель рельief (DEM) и определение высотных зон риска
dem_data = {
    'id': [1],
    'geometry': [Point(50.7489, 60.6117)],
    'elevation': [200]  # примерное значение высоты в метрах над уровнем моря
}

dem_gdf = gpd.GeoDataFrame(dem_data, geometry='geometry')

# 3. Определение расстояния от каждого поля до реки Уржар
def distance_to_river(row):
    return np.sqrt((row.geometry.x - river_coords[0])**2 + (row.geometry.y - river_coords[1])**2)

river_coords = (50.7489, 60.6117)  # примерные координаты реки Уржар
fields_gdf['distance_to_river'] = fields_gdf.apply(distance_to_river, axis=1)

# 4. Оценка рисков засоления почв
def risk_assessment(row):
    crop_coeff = {'пшеница': 0.6, 'кукуруза': 0.8, 'овес': 0.7}  # коэффициенты зависимости культур от воды
    water_stress = row['water_consumption'] / (row['distance_to_river'] * crop_coeff[row['crop_type']])
    if water_stress > 1:
        return 'Высокий риск'
    elif water_stress > 0.5:
        return 'Средний риск'
    else:
        return 'Низкий риск'

fields_gdf['risk_level'] = fields_gdf.apply(risk_assessment, axis=1)

# 5. Визуализация результатов на карте с использованием библиотеки `folium`
m = folium.Map(location=[50.7489, 60.6117], zoom_start=13)

for idx, row in fields_gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue' if row['risk_level'] == 'Низкий риск' else ('orange' if row['risk_level'] == 'Средний риск' else 'red'),
        fill=True
    ).add_to(m)

m.save("195.html")