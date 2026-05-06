import pandas as pd
from folium import Map, CircleMarker
import geopandas as gpd

# Загрузка данных о параметрах воды в реке Талгар
data = {
    'pH': [7.2, 6.8, 7.5, 6.9, 7.1],
    'температура': [15, 12, 18, 14, 16],
    'прозрачность': [80, 90, 85, 88, 82],
    'нитраты': [10, 8, 12, 9, 11]
}
df = pd.DataFrame(data)

# Создание геообработки для карты загрязнения сточными водами
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['пH'], df['температура']))

# Создание карты с помощью библиотеки Folium
m = Map(location=[43.0, 76.5], zoom_start=10)

# Добавление маркеров на карте для каждого наблюдения
for i in range(len(gdf)):
    CircleMarker([gdf.geometry.iloc[i].y, gdf.geometry.iloc[i].x],
                 radius=gdf['нитраты'].iloc[i] * 0.1,
                 color='red').add_to(m)

# Визуализация результатов на карте
m.save("40.html")