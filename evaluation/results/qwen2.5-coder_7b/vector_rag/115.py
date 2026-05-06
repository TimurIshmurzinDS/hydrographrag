import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географическими границами бассейнов
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление географических границ бассейнов на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты сельских населенных пунктов (Temirlik village)
temirlik_villages = [
    {'name': 'Temirlik village 1', 'geometry': wkt.loads('POINT(37.5648 40.9234)')},
    {'name': 'Temirlik village 2', 'geometry': wkt.loads('POINT(37.5748 40.9334)')},
    {'name': 'Temirlik village 3', 'geometry': wkt.loads('POINT(37.5848 40.9434)')}
]

# Определение, какие сельские населенные пункты находятся внутри географических границ бассейнов
for village in temirlik_villages:
    if basin_data.geometry.contains(village['geometry']).any():
        folium.Marker([village['geometry'].y, village['geometry'].x], popup=village['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("115.html")