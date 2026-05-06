import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка с координатами (WKT) реки Aksu River
wkt_coords = [
    {'type': 'Point', 'coordinates': [45.123, 69.456]},
    {'type': 'Point', 'coordinates': [45.234, 69.567]}
]

# Добавление координат на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coordinates'], popup='Aksu River').add_to(m)

# Сохранение карты в файл
m.save("197.html")