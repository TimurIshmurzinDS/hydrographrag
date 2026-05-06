import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейнах
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине первого геометрии
centroid = basin_data.geometry.iloc[0].centroid
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coordinates = [
    {"name": "Координаты 1", "geometry": wkt.loads("POINT(45.1234 30.5678)")},
    {"name": "Координаты 2", "geometry": wkt.loads("POINT(40.9876 35.4321)")},
]

# Добавление координат на карту
for coord in wkt_coordinates:
    folium.Marker(location=[coord['geometry'].coords[0][1], coord['geometry'].coords[0][0]],
                  popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("145.html")