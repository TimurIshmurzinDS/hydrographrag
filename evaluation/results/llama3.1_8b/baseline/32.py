import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Сбор данных о параметрах воды в реке Талгар
data = {
    'location': ['Талгар', 'Алматы', 'Кок-Жайык'],
    'pH': [7.2, 6.8, 7.5],
    'кислорода': [10, 12, 9],
    'температура': [15, 18, 16]
}

df = pd.DataFrame(data)

# Анализ данных
print(df.describe())

# Создание гео-данных для мониторинга
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['location'].str.split(',').str[1].astype(float), df['location'].str.split(',').str[0].astype(float))
)

# Визуализация результатов на карте с помощью Folium
m = Map(location=[43.25, 76.95], zoom_start=10)
for index, row in gdf.iterrows():
    Marker(row.geometry).add_to(m)

# Сохранение карты в файл
m.save("32.html")