import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с зеленой заливкой и темно-зеленой линией
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Бассейн',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
coordinates = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 55.7634, 'lon': 37.6235},
    {'lat': 55.7711, 'lon': 37.6297}
]

# Добавление маркеров на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("37.html")