import geopandas as gpd
import folium

# Загрузка топографической сети притоков реки Тентек (пример файла shapefile)
topography_network = gpd.read_file('path_to_topography_network.shp')

# Загрузка данных о спутнике (пример файла CSV с координатами)
satellite_data = pd.read_csv('path_to_satellite_data.csv')

# Пример данных о спутнике
# satellite_data = {
#     'time': ['2023-10-01 12:00:00', '2023-10-01 12:05:00'],
#     'latitude': [47.6062, 47.6065],
#     'longitude': [-122.3321, -122.3324]
# }

# Создание карты
m = folium.Map(location=[topography_network.geometry.centroid.y.mean(), topography_network.geometry.centroid.x.mean()], zoom_start=10)

# Добавление топографической сети на карту
folium.GeoJson(topography_network).add_to(m)

# Добавление точек спутника на карту
for index, row in satellite_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['time']).add_to(m)

# Сохранение карты в HTML файл
m.save("250.html")