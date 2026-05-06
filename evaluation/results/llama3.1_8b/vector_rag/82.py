import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с рекой в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте hardcoded список словарей с координатами постов
posts = [
    {'name': 'Post 1', 'coordinates': (43.1234, 79.5678)},
    {'name': 'Post 2', 'coordinates': (43.2345, 80.0123)}
]

# Добавьте посты на карту
for post in posts:
    folium.Marker(post['coordinates'], popup=post['name']).add_to(m)

# Проверьте, превышает ли расход воды на каждом посту критическую отметку паводка
critical_water_level = 1000  # Критическая отметка паводка в см

for post in posts:
    water_consumption_value = 500  # Значение потребления воды на посту в см
    if water_consumption_value > critical_water_level:
        folium.Marker(post['coordinates'], popup=f'{post["name"]}: Рисок превышает критическую отметку паводка').add_to(m)

# Сохраните карту в файл
m.save("82.html")