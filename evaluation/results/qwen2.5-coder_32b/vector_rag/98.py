import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах
basins = gpd.read_file(r"data/basin_data.shp")
basins = basins.to_crs('EPSG:4326')

# Инициализация карты с центром в среднем значении координат бассейнов
centroid = basins.geometry.centroid.unary_union.centroid
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейнов на карту
folium.GeoJson(basins.to_json(), name="Basins", style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2,
}).add_to(m)

# Сохранение карты в файл
m.save("98.html")