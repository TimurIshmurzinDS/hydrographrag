import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне реки Тентек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты разветвления притоков реки Тентек в формате WKT
forks_wkt = [
    "LINESTRING (75.9184 43.0622, 75.9200 43.0630)",
    "LINESTRING (75.9184 43.0622, 75.9170 43.0630)"
]

# Преобразование WKT в геометрические объекты и добавление на карту
forks = [gpd.GeoSeries(wkt.loads(fork), crs='EPSG:4326') for fork in forks_wkt]
for fork in forks:
    folium.PolyLine(locations=fork.geometry.apply(lambda x: (x.y, x.x)).tolist(), color="blue", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в HTML файл
m.save("242.html")