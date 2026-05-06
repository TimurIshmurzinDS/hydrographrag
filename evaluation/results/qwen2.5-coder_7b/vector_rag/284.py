import geopandas as gpd
import folium
from shapely import wkt

# Загрузка геоданных о бассейне на Марсе
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна и использованием тайла 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат (WKT) для демонстрации
coordinates = [
    {'name': 'Point_1', 'wkt': 'POINT(35.4678 56.7890)'},
    {'name': 'Point_2', 'wkt': 'POINT(37.1234 58.9012)'}
]

# Преобразование координат в GeoDataFrame
coords_gdf = gpd.GeoDataFrame(coordinates, geometry=[wkt.loads(coord['wkt']) for coord in coordinates])

# Добавление точек на карту
for idx, row in coords_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Сохранение карты в файл
m.save("284.html")