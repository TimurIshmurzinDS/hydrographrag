import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile в геопандас
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине области
centroid = basin_data.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.__geo_interface__,
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами (WKT)
wkt_coordinates = [
    {"lat": 55.7558, "lon": 37.6173},
    {"lat": 55.7631, "lon": 37.6255},
    {"lat": 55.7642, "lon": 37.6337}
]

# Добавление маркеров на карту
for coord in wkt_coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("139.html")