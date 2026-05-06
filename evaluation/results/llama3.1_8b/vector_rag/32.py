import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами и экологическими данными (предположим, что у нас есть доступ к этим данным)
coordinates = [
    {'lat': 43.1234, 'lon': 76.5678, 'temperature': 15, 'oxygen': 10, 'nitrate': 5, 'phosphate': 2},
    {'lat': 43.2345, 'lon': 76.6789, 'temperature': 16, 'oxygen': 11, 'nitrate': 6, 'phosphate': 3},
    {'lat': 43.3456, 'lon': 76.7890, 'temperature': 17, 'oxygen': 12, 'nitrate': 7, 'phosphate': 4},
    {'lat': 43.4567, 'lon': 76.8901, 'temperature': 18, 'oxygen': 13, 'nitrate': 8, 'phosphate': 5},
    {'lat': 43.5678, 'lon': 77.0012, 'temperature': 19, 'oxygen': 14, 'nitrate': 9, 'phosphate': 6}
]

# Добавить точки на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup=f"Температура: {coord['temperature']}, Кислород: {coord['oxygen']}, Нитраты: {coord['nitrate']}, Фосфаты: {coord['phosphate']}").add_to(m)

# Сохранить карту в файл
m.save("32.html")