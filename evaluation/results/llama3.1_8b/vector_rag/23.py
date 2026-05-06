import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с бассейном
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Создание списка наблюдательных пунктов
observation_points = [
    {"name": "Наблюдательный пункт 1", "location": wkt.loads("POINT(55.123456 37.654321)")},
    {"name": "Наблюдательный пункт 2", "location": wkt.loads("POINT(55.123456 37.654321)")},
    {"name": "Наблюдательный пункт 3", "location": wkt.loads("POINT(55.123456 37.654321)")},
    {"name": "Наблюдательный пункт 4", "location": wkt.loads("POINT(55.123456 37.654321)")}
]

# 4. Добавление наблюдательных пунктов на карту
for point in observation_points:
    folium.Marker(point["location"], popup=point["name"]).add_to(m)

# 5. Сохранение карты в файл
m.save("23.html")