import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ ровнинного участка
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границ ровнинного участка
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание маркера для города Talgar (пример координат)
talgar_coords = [(51.4976, 73.3889), (51.4976, 73.3889), (51.4976, 73.3889), (51.4976, 73.3889)]
for coord in talgar_coords:
    folium.Marker(coord, popup='г. Talgar').add_to(m)

# Сохранение карты
m.save("10.html")