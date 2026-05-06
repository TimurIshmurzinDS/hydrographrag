import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о водосборе
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине водосбора и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить водосбор на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами точки наблюдения
points = [
    {'lat': 46.1234, 'lon': 73.4567},
]

# Добавить точки на карту
for point in points:
    folium.Marker(point).add_to(m)

# Добавить отметку о уровне паводка на реке Шарын
folium.Marker([46.1234, 73.4567], popup='Уровень паводка: 10 метров').add_to(m)

# Сохранить карту в файл
m.save("226.html")