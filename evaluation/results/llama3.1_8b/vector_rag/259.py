import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о водосборном бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине водосборного бассейна
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление водосборного бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создание списка с координатами (WKT) для реки Баскан (hardcoded)
wkt_coords = [
    {'type': 'Feature', 'geometry': wkt.loads('POLYGON ((48.123 77.456, 48.124 77.457, 48.125 77.458, 48.126 77.459, 48.127 77.460))')},
]

# Добавление координат на карту
for coord in wkt_coords:
    folium.Marker(location=coord['geometry'].coords[0], popup='Река Баскан').add_to(m)

# Сохранение карты в файл
m.save("259.html")