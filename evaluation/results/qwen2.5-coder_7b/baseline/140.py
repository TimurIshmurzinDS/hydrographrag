import folium
from shapely.geometry import Point
from geopandas import GeoDataFrame

# Пример данных о местоположении датчиков и времени последней активности
data = {
    'id': [1, 2, 3, 4, 5],
    'latitude': [40.7128, 40.7130, 40.7132, 40.7134, 40.7136],
    'longitude': [-74.0060, -74.0058, -74.0056, -74.0054, -74.0052],
    'last_activity': ['2023-01-01 12:00', '2023-01-01 12:01', '2023-01-01 12:02', '2023-01-01 12:03', '2023-01-01 12:04']
}

# Создание GeoDataFrame
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = GeoDataFrame(data, geometry=geometry)

# Определение радиуса действия датчиков (в метрах)
radius = 500

# Функция для проверки стабильности связи
def check_stability(gdf, radius):
    stable_sensors = []
    for i in range(len(gdf)):
        sensor1 = gdf.iloc[i]
        for j in range(i + 1, len(gdf)):
            sensor2 = gdf.iloc[j]
            if sensor1.geometry.distance(sensor2.geometry) <= radius:
                if (sensor1['last_activity'] > sensor2['last_activity']) and (sensor2['last_activity'] > sensor1['last_activity']):
                    stable_sensors.append((sensor1['id'], sensor2['id']))
    return stable_sensors

# Проверка стабильности связи
stable_sensors = check_stability(gdf, radius)

# Визуализация на карте
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=13)

for idx, row in gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Sensor {row['id']}", icon=folium.Icon(color='red')).add_to(m)

# Подсветка стабильных связей
for sensor_pair in stable_sensors:
    sensor1 = gdf[gdf['id'] == sensor_pair[0]]
    sensor2 = gdf[gdf['id'] == sensor_pair[1]]
    folium.PolyLine([sensor1.geometry.iloc[0], sensor2.geometry.iloc[0]], color='green', weight=5).add_to(m)

# Сохранение карты
m.save("140.html")