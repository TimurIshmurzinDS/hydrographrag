import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_json(), name='bass').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 74.5678},
    {'lat': 43.2345, 'lon': 75.6789}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Точка').add_to(m)

# Сохранить карту в файл
m.save("113.html")