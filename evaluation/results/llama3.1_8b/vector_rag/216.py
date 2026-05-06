import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области водоёма на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt.values.tolist(),
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {"lat": 43.1234, "lon": 79.5678},
    {"lat": 43.2345, "lon": 80.6789}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("216.html")