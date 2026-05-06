import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 44.5678, 'lon': 77.9012}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("248.html")