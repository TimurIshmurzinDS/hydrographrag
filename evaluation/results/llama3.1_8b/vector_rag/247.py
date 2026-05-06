import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.233333, 'lon': 76.666667},
    {'lat': 43.283333, 'lon': 76.716667},
    {'lat': 43.333333, 'lon': 76.766667}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("247.html")