import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне (только границы)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты притоков реки Каскелен (пример данных)
kaskelen_sources = [
    {'name': 'Приток 1', 'wkt': 'POINT(37.5648 49.0123)'},
    {'name': 'Приток 2', 'wkt': 'POINT(37.5748 49.0223)'},
    {'name': 'Приток 3', 'wkt': 'POINT(37.5848 49.0323)'}
]

# Преобразование WKT в объекты Shapely
kaskelen_sources_gdf = gpd.GeoDataFrame(kaskelen_sources, geometry=[wkt.loads(point['wkt']) for point in kaskelen_sources])

# Добавление притоков на карту
for idx, row in kaskelen_sources_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Сохранение карты
m.save("247.html")