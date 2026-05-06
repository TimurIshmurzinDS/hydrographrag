import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile в GeoPandas DataFrame
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине области и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_child(
    folium.features.GeoJsonTooltip(fields=['name'], aliases=['Название'], labels=True)
).add_to(m)

# Создание списка наблюдательных точек в виде словарей
observations = [
    {'location': wkt.loads('POINT(54.123 36.456)'), 'river': 'Osek River'},
    {'location': wkt.loads('POINT(55.789 37.012)'), 'river': 'Koktal River'},
    {'location': wkt.loads('POINT(53.321 35.678)'), 'river': 'Osek River'}
]

# Добавление наблюдательных точек на карту
for observation in observations:
    folium.Marker(observation['location'], popup=f'Река: {observation["river"]}, Наблюдение').add_to(m)

# Сохранение карты в файл
m.save("73.html")