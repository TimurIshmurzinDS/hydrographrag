import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с историческими данными реки Дос
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_crs(epsg=3857).geometry.__geo_interface__,
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT) точек измерения уровня воды в реке Лепсы на 2025 год
lepsy_data = [
    {'name': 'Point1', 'wkt': 'POINT(55.1234 37.5678)', 'water_level': 10},
    {'name': 'Point2', 'wkt': 'POINT(55.2345 37.6789)', 'water_level': 15}
]

# Добавить точки на карту
for point in lepsy_data:
    folium.Marker(location=wkt.loads(point['wkt']).coords[0], popup=f'Уровень воды: {point["water_level"]}').add_to(m)

# Сохранить карту в файл
m.save("124.html")