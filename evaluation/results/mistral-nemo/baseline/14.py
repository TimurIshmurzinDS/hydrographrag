import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('batareyka_river_data.csv')  # Замените 'batareyka_river_data.csv' на путь к вашему файлу данных
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Шаг 2: Анализ данных
# Предполагается, что в данных есть столбцы 'water_quality' и 'river_level'
problematic_locations = gdf[(gdf['water_quality'] < 5) | (gdf['river_level'] > 10)]

# Шаг 3: Визуализация данных
m = folium.Map(location=[55.7821, 49.1257], zoom_start=12)  # Замените координаты на центр вашей карты

for idx, row in problematic_locations.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Качество воды: {row["water_quality"]}, Уровень реки: {row["river_level"]}').add_to(m)

# Шаг 4: Сохранение карты
m.save("14.html")