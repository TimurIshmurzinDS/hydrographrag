import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна рек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек на карте для визуализации (например, местоположение рек)
# В реальном сценарии эти данные должны быть получены из дополнительных источников
coordinates = [
    {'name': 'Karaoy River', 'coords': [42.8500, 76.9300]},
    {'name': 'Baskan River', 'coords': [42.8700, 76.9500]},
    {'name': 'Temirlik River', 'coords': [42.8900, 76.9700]}
]

# Добавление маркеров для каждой из рек на карту
for coord in coordinates:
    folium.Marker(
        location=coord['coords'],
        popup=coord['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("90.html")