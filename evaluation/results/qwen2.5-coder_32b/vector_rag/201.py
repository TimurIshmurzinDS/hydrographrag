import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о границах бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), добавляем их на карту
# В данном контексте нет конкретных координат, но пример:
# coordinates = [{'name': 'Aул Лепсы', 'wkt': 'POINT(76.5 42.8)'}]
# for coord in coordinates:
#     point = wkt.loads(coord['wkt'])
#     folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("201.html")