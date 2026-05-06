import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине области и использованием плиток CartoDB positron
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.__geo_interface__,
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123456, 'lon': 37.654321},
    {'lat': 55.987654, 'lon': 38.765432}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("233.html")