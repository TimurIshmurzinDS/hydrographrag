import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами постов (в данном случае hardcoded)
posts = [
    {'name': 'Пост 1', 'coords': wkt.loads('POINT(48.6784 45.0323)')},
    {'name': 'Пост 2', 'coords': wkt.loads('POINT(48.6798 45.0337)')},
    {'name': 'Пост 3', 'coords': wkt.loads('POINT(48.6812 45.0351)')}
]

# Рассчитать расход воды для каждого поста
for post in posts:
    # Расчет площади бассейна (в данном случае hardcoded)
    basin_area = 1000
    
    # Расчет длины реки (в данном случае hardcoded)
    river_length = 50
    
    # Расчет высоты воды в посту и устье (в данном случае hardcoded)
    water_height_post = 10
    water_height_ustie = 5
    
    # Рассчитать расход воды по формуле
    flow_rate = (basin_area / river_length) * (water_height_post / water_height_ustie)
    
    # Добавить маркер на карту с информацией о расходе воды
    folium.Marker(location=[post['coords'].y, post['coords'].x], popup=f'Расход воды: {flow_rate} м³/с').add_to(m)

# Сохранить карту в файл
m.save("78.html")