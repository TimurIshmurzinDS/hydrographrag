import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd

# Шаг 1: Сбор данных о расходе воды в реке Каратал.
data = {
    'river': ['Каратал'],
    'water_flow': [1000]  # в кубических метрах в секунду
}
df = pd.DataFrame(data)

# Шаг 2: Создание географической модели потока воды в реке Каратал.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['river'].str.get(0), df['water_flow']))

# Шаг 3: Анализ данных для определения оптимального количества воды, необходимого для приготовления супа.
optimal_water_flow = 500  # в кубических метрах в секунду

# Шаг 4: Визуализация результатов на карте с помощью библиотеки Folium.
m = Map(location=[46.5, 76.0], zoom_start=10)
for index, row in gdf.iterrows():
    if row['water_flow'] > optimal_water_flow:
        Marker([row.geometry.y, row.geometry.x]).add_to(m)

# Сохранение карты в файл.
m.save("214.html")