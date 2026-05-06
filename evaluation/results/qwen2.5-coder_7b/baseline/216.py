import folium
from geopandas import GeoDataFrame, Point
from shapely.geometry import LineString

# Пример данных от сенсоров реки Karaoy River (в реальном случае данные будут получены из API или файлов)
sensor_data = {
    'latitude': [39.1234, 39.1256, 39.1278],
    'longitude': [105.6789, 105.6801, 105.6813]
}

# Создаем GeoDataFrame с данными о местоположении сенсоров
sensor_gdf = GeoDataFrame(sensor_data, geometry=[Point(xy) for xy in zip(sensor_data['longitude'], sensor_data['latitude'])])

# Определяем начальное и конечное положения для телепортации
start_point = Point(105.6789, 39.1234)
end_point = Point(105.6813, 39.1278)

# Создаем маршрут как линию между начальным и конечным точками
route = LineString([start_point, end_point])

# Создаем карту с использованием folium
m = folium.Map(location=[sensor_gdf.geometry.centroid.y.mean(), sensor_gdf.geometry.centroid.x.mean()], zoom_start=15)

# Добавляем маркеры для сенсоров
for idx, row in sensor_gdf.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Sensor {idx+1}').add_to(m)

# Добавляем маршрут на карту
folium.PolyLine(route.coords, color='blue', weight=2.5, opacity=1).add_to(m)

# Сохраняем карту в файл HTML
m.save("216.html")