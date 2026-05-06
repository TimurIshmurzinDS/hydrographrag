import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если бы были координаты (WKT), они были бы добавлены следующим образом:
# coordinates = [{'name': 'Butak village', 'wkt': 'POINT(37.618423 55.755814)'}]
# for coord in coordinates:
#     point = wkt.loads(coord['wkt'])
#     folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("192.html")