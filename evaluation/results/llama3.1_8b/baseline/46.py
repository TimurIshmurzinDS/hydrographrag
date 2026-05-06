import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузим данные о уровнях воды для обоих лет.
data_2022 = pd.read_csv('sarykan_river_water_levels_2022.csv')
data_2023 = pd.read_csv('sarykan_river_water_levels_2023.csv')

# Преобразуем данные в геопandas DataFrame
gdf_2022 = gpd.GeoDataFrame(data_2022, geometry=gpd.points_from_xy(data_2022.Longitude, data_2022.Latitude))
gdf_2023 = gpd.GeoDataFrame(data_2023, geometry=gpd.points_from_xy(data_2023.Longitude, data_2023.Latitude))

# Создадим слой данных для каждого года и добавим его на карту
m = folium.Map(location=[46.0, 70.0], zoom_start=10)
folium.GeoJson(gdf_2022.to_crs(epsg=4326)).add_to(m)
folium.GeoJson(gdf_2023.to_crs(epsg=4326)).add_to(m)

# Используем функцию сравнения слоев данных для определения различий между уровнями воды за два года
def compare_layers(layer1, layer2):
    return folium.FeatureGroup(
        name='Сравнение уровней воды',
        show=True,
        overlay=True,
        control=False).add_to(m)

compare_layers(gdf_2022, gdf_2023)

# Визуализируем результаты на карте
m.save("46.html")