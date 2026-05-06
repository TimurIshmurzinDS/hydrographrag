import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='Basin').add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {'location': wkt.loads('POINT(100.0 50.0)')},
    {'location': wkt.loads('POINT(101.0 51.0)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['location'].coords, icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("271.html")