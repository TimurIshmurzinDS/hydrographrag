import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.geometry.__geo_interface__, name='bass').add_to(m)

# Создание списка координат для кратчайшего пути
coordinates = [
    {'lat': 3.23, 'lon': 5.67},  # Координаты созвездия Ориона
    {'lat': 4.12, 'lon': 6.34}   # Координаты реки Шилик
]

# Добавление кратчайшего пути на карту
folium.PolyLine(coordinates).add_to(m)

# Сохранение карты в файл
m.save("246.html")