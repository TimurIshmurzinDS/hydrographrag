import geopandas as gpd
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка точек (WKT) для реки Эмел и Тентека
emel_points = [
    {'name': 'Эмел', 'geometry': wkt.loads('POINT(55.123 37.456)')},
    {'name': 'Тентек', 'geometry': wkt.loads('POINT(56.789 38.901)')}
]

byzhy_points = [
    {'name': 'Быж', 'geometry': wkt.loads('POINT(54.321 36.654)')}
]

# Добавление точек на карту
for point in emel_points:
    folium.Marker(point['geometry'].coords[0], popup=point['name']).add_to(m)

for point in byzhy_points:
    folium.Marker(point['geometry'].coords[0], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("101.html")