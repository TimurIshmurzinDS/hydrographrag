import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Подготовка данных
data = {
    'location': ['Пункт 1', 'Пункт 2', 'Пункт 3'],
    'level_of_pollution': [10, 20, 30],
    'type_of_pollutant': ['Химический', 'Биологический', 'Физический']
}
df = pd.DataFrame(data)

# Создание географической модели
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['location'].str.split(',').astype(float).iloc[:, 0], df['location'].str.split(',').astype(float).iloc[:, 1]))

# Анализ влияния загрязнения
def calculate_pollution_impact(level_of_pollution):
    if level_of_pollution < 15:
        return 'Низкий'
    elif level_of_pollution < 30:
        return 'Средний'
    else:
        return 'Высокий'

gdf['pollution_impact'] = gdf['level_of_pollution'].apply(calculate_pollution_impact)

# Визуализация результатов
m = Map(location=[55.7558, 37.6173], zoom_start=10)
for index, row in gdf.iterrows():
    Marker([row.geometry.y, row.geometry.x], popup=f'Пункт {index+1}: {row["pollution_impact"]}').add_to(m)

m.save("186.html")