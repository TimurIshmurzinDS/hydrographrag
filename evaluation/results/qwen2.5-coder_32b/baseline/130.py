import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Предположим, что у нас есть данные о уровнях воды рек в формате CSV
# Структура данных: дата, долгота, широта, уровень_воды (для каждой из рек)

# Загрузка данных
bayankol_data = pd.read_csv('bayankol_water_levels.csv')
shilik_data = pd.read_csv('shilik_water_levels.csv')

# Преобразование данных в GeoDataFrame
bayankol_gdf = gpd.GeoDataFrame(
    bayankol_data, geometry=[Point(xy) for xy in zip(bayankol_data['longitude'], bayankol_data['latitude'])]
)
shilik_gdf = gpd.GeoDataFrame(
    shilik_data, geometry=[Point(xy) for xy in zip(shilik_data['longitude'], shilik_data['latitude'])]
)

# Предположим, что у нас есть базовый уровень воды реки Shilik
base_level_shilik = shilik_gdf['water_level'].mean()

# Вычисление отклонений уровня воды реки Bayankol относительно базового уровня реки Shilik
bayankol_gdf['deviation'] = bayankol_gdf['water_level'] - base_level_shilik

# Создание карты с отметками исторических отклонений
m = folium.Map(location=[bayankol_gdf['latitude'].mean(), bayankol_gdf['longitude'].mean()], zoom_start=10)

# Добавление маркеров на карту для каждого измерения уровня воды реки Bayankol
for _, row in bayankol_gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='blue' if row['deviation'] < 0 else 'red',
        fill=True,
        fill_color='blue' if row['deviation'] < 0 else 'red',
        popup=f"Date: {row['date']}\nLevel: {row['water_level']}\nDeviation: {row['deviation']:.2f}"
    ).add_to(m)

# Сохранение карты в файл
m.save("130.html")