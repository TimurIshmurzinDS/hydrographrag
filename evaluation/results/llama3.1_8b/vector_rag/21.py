import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту как GeoJSON с зеленой заливкой и темно-зеленой линией
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.apply(lambda x: wkt.dumps(x)).tolist(),
                name='Бассейн',
                style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT) рек
river_coords = [
    {'name': 'Shyzhyn River', 'coords': wkt.loads('POINT(48.6784 35.0333)')},
    {'name': 'Shynzhaly River', 'coords': wkt.loads('POINT(48.6922 34.9833)')},
    {'name': 'Byzhy River', 'coords': wkt.loads('POINT(48.6989 34.9583)')}
]

# Добавление координат рек на карту
for river in river_coords:
    folium.Marker(location=river['coords'].coords[0], popup=river['name']).add_to(m)

# Сохранение карты в файл
m.save("21.html")