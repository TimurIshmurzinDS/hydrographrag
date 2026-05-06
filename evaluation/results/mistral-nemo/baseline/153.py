import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Подготовка данных
data = {
    'name': ['Sarykan River', 'River A', 'River B', 'River C'],
    'avg_flow': [100, 50, 75, 80],
    'flood_index': [2.5, 1.8, 3.2, 2.1]
}
df = pd.DataFrame(data)

geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Шаг 2: Определение индекса половодья
gdf['flood_index'] = gdf['max_flow'] / gdf['avg_flow']

# Шаг 3: Классификация рек
gdf['flood_classification'] = pd.cut(gdf['flood_index'], bins=[0, 2, 4], labels=['Low', 'Medium', 'High'])

# Шаг 4: Визуализация результатов
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

for idx, row in gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x],
                  popup=f'River: {row.name}<br>Flood Index: {row.flood_index:.2f}<br>Flood Classification: {row.flood_classification}').add_to(m)

m.save("153.html")