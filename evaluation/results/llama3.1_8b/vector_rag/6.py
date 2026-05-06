import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с бассейном в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name='Basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("6.html")