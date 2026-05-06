import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Сбор данных
data = {
    'river': ['Курты', 'Уржар'],
    'level_change': [10, 20],
    'date': ['2022-01-01', '2022-01-15']
}
df = pd.DataFrame(data)

# Анализ данных
max_level_change = df['level_change'].max()
min_level_change = df['level_change'].min()

# Обработка данных
df['stress_level'] = (df['level_change'] - min_level_change) / (max_level_change - min_level_change)

# Моделирование
model = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['river'].str.get(0), df['date']))

# Визуализация
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in model.iterrows():
    marker = CircleMarker(row.geometry, radius=row['stress_level'] * 1000000)
    m.add_child(marker)

m.save("108.html")