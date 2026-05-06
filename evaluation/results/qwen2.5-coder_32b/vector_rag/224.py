import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты реки Karaoy в формате WKT
karaoy_coords_wkt = "LINESTRING (37.5 41.0, 38.0 41.5, 38.5 42.0)"  # Примерные координаты для демонстрации
karaoy_line = wkt.loads(karaoy_coords_wkt)

# Создание слоя с рекой Karaoy на карте
folium.GeoJson(gpd.GeoSeries([karaoy_line], crs='EPSG:4326').to_json(), name="Karaoy River", style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("224.html")