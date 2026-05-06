import geopandas as gpd
import folium
from folium.plugins import HeatMap
import numpy as np

# Загрузка данных о реках (пример данных)
shynzhaly_river = gpd.read_file("path_to_shynzhaly_river.shp")
shyzhyn_river = gpd.read_file("path_to_shyzhyn_river.shp")

# Пример данных о топографии и исторических наводнениях (замените на реальные данные)
topography_data = {
    'geometry': [shynzhaly_river.geometry, shyzhyn_river.geometry],
    'elevation': [1000, 800],  # Пример высоты над уровнем моря
    'flood_history': [5, 3]  # Пример количества исторических наводнений
}

topography_gdf = gpd.GeoDataFrame(topography_data)

# Создание карты для визуализации
m = folium.Map(location=[topography_gdf.geometry.centroid.y.mean(), topography_gdf.geometry.centroid.x.mean()], zoom_start=10)

# Визуализация топографии и исторических наводнений
for idx, row in topography_gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        radius=row['elevation'] / 50,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Река: {topography_gdf.columns[idx]}, Высота: {row['elevation']} м, Наводнения: {row['flood_history']}"
    ).add_to(m)

# Визуализация вероятности наводнений (пример данных)
flood_probability = np.random.rand(len(topography_gdf)) * 0.5 + 0.25

for idx, row in topography_gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        radius=flood_probability[idx] * 100,
        color='red',
        fill=True,
        fill_color='red',
        popup=f"Река: {topography_gdf.columns[idx]}, Вероятность наводнения: {flood_probability[idx]:.2f}"
    ).add_to(m)

# Сохранение карты
m.save("154.html")