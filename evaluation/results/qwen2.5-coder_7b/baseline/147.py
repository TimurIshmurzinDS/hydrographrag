import pandas as pd
import folium
from geopandas import GeoDataFrame
from shapely.geometry import Point

# Загрузка данных с датчиков (пример)
data = {
    'sensor_id': [1, 2, 3, 4, 5],
    'latitude': [50.123, 50.456, 50.789, 51.123, 51.456],
    'longitude': [49.123, 49.456, 49.789, 50.123, 50.456],
    'value': [10, 20, 30, 40, 50]
}
df = pd.DataFrame(data)

# Определение границ района (пример)
center_lat, center_lon = 50.5, 49.5
radius_km = 50

# Создание геодатафрейма для данных датчиков
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf_sensors = GeoDataFrame(df, geometry=geometry)

# Определение границ района в виде круга
from shapely.geometry import Point, Polygon
circle_center = Point(center_lon, center_lat)
circle_radius = radius_km * 1000  # радиус в метрах
circle = circle_center.buffer(circle_radius)

# Фильтрация данных по радиусу
gdf_filtered = gdf_sensors[gdf_sensors.geometry.within(circle)]

# Анализ ошибок (пример: выбросы)
from scipy import stats
z_scores = np.abs(stats.zscore(gdf_filtered['value']))
filtered_data = gdf_filtered[z_scores < 3]

# Визуализация на карте
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

for idx, row in filtered_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Sensor ID: {row['sensor_id']}, Value: {row['value']}").add_to(m)

m.save("147.html")