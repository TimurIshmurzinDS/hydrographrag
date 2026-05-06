import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Бассейн реки Shilik',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами (WKT)
coordinates = [
    {"lat": 43.1234, "lon": 76.5432},
    {"lat": 43.1245, "lon": 76.5443},
    # Добавьте остальные координаты в этот список
]

# Создание карты с координатами (WKT)
m.add_child(folium.Marker(
    location=[43.1234, 76.5432],
    popup='Координата 1',
    icon=folium.Icon(color='red')
))

# Сохранение карты в файл
m.save("59.html")