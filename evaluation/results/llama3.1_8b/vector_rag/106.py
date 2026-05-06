import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile в GeoPandas DataFrame с преобразованием в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты Folium с центром в середине площади
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат WKT (в данном случае hardcoded)
wkt_coords = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавление маркеров на карту для координат WKT
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("106.html")