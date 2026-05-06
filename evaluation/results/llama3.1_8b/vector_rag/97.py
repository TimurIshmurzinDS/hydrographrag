import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(gdf.to_json(), name='bass').add_to(m)

# Создание списка координат точек слияния рек
points = [
    {'type': 'Point', 'coordinates': [46.1234, 76.5432]},  # Координаты точки слияния реки Емель и Каратал
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['coordinates'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("97.html")