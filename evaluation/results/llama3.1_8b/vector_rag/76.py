import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список гидропостов с их текущим расходом воды
hydro_posts = [
    {'id': 1, 'name': 'Гидропост 1', 'water_level': 10.5, 'water_consumption': 50},
    {'id': 2, 'name': 'Гидропост 2', 'water_level': 12.8, 'water_consumption': 75},
    {'id': 3, 'name': 'Гидропост 3', 'water_level': 9.2, 'water_consumption': 30}
]

# Добавить гидропосты на карту
for hydro_post in hydro_posts:
    folium.Marker(location=[hydro_post['water_level'], hydro_post['water_consumption']], popup=f"Гидропост {hydro_post['name']}: Уровень воды - {hydro_post['water_level']} м, Расход воды - {hydro_post['water_consumption']} м³/с").add_to(m)

# Сохранить карту в файл
m.save("76.html")