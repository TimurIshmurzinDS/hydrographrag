import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {"lat": 46.5, "lon": 78.7},
    {"lat": 46.6, "lon": 78.8},
    {"lat": 46.7, "lon": 78.9}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Маркер').add_to(m)

# Сохранение карты в файл
m.save("236.html")