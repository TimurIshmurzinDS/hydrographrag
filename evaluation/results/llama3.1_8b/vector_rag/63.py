import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с данными о бассейне в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей с координатами и названиями гидропостов (в данном случае hardcoded)
hydro_posts = [
    {'name': 'Гидропост 1', 'coords': [48.1234, 36.5678]},
    {'name': 'Гидропост 2', 'coords': [47.9012, 37.3456]}
]

# Добавьте гидропосты на карту
for hydro_post in hydro_posts:
    folium.Marker(location=hydro_post['coords'], popup=f"{hydro_post['name']}: {hydro_post['level']} см").add_to(m)

# Рассчитайте текущие уровни воды для каждого гидропоста (в данном случае hardcoded)
levels = {
    'Гидропост 1': 150,
    'Гидропост 2': 200
}

# Добавьте информацию о уровнях воды на карту
for hydro_post in hydro_posts:
    folium.Marker(location=hydro_post['coords'], popup=f"{hydro_post['name']}: {levels[hydro_post['name']]} см").add_to(m)

# Сохраните карту в файл
m.save("63.html")