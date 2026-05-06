import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из файла shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Karatal
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что координаты аномалии уровня воды в реке Karatal известны и представлены в формате WKT
anomaly_coordinates = "POINT(85.3456 47.1234)"  # Примерные координаты для демонстрации

# Создание слоя с аномалией уровня воды
anomaly_point = gpd.GeoSeries([wkt.loads(anomaly_coordinates)], crs='EPSG:4326')
folium.Marker(location=[anomaly_point.y.iloc[0], anomaly_point.x.iloc[0]], popup="Аномалия уровня воды", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("222.html")