import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Пример данных: исторические данные о наводнениях и топография реки
data = {
    'geometry': [Point(10.5, 48.2), Point(10.6, 48.3), Point(10.7, 48.4)],
    'water_level': [100, 110, 120],
    'flooded': [True, True, False]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Пример данных о высоте водного уровня и интенсивности осадков
weather_data = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'water_level': [95, 105, 115],
    'precipitation': [10, 20, 30]
}

# Создание DataFrame
weather_df = pd.DataFrame(weather_data)

# Пример данных о топографии (просто для демонстрации)
topography_data = {
    'geometry': [Point(10.5, 48.2), Point(10.6, 48.3), Point(10.7, 48.4)],
    'elevation': [100, 110, 120]
}

# Создание GeoDataFrame
topo_gdf = gpd.GeoDataFrame(topography_data, geometry='geometry')

# Пример функции для оценки риска наводнения
def calculate_flood_risk(gdf, weather_df):
    risk_scores = []
    for index, row in gdf.iterrows():
        water_level = row['water_level']
        elevation = topo_gdf[topo_gdf.geometry.intersects(row['geometry'])]['elevation'].values[0]
        precipitation = weather_df['precipitation'].max()
        
        # Простой алгоритм для оценки риска
        if water_level + precipitation > elevation:
            risk_scores.append(1)
        else:
            risk_scores.append(0)
    
    gdf['risk'] = risk_scores
    return gdf

# Оценка риска наводнения
flood_risk_gdf = calculate_flood_risk(gdf, weather_df)

# Визуализация результатов на карте
m = folium.Map(location=[48.25, 10.6], zoom_start=13)

for idx, row in flood_risk_gdf.iterrows():
    if row['risk'] == 1:
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)
    else:
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            color='green',
            fill=True,
            fill_color='green'
        ).add_to(m)

m.save("23.html")