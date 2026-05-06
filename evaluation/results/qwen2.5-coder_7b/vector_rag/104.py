import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географическими объектами
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Инициализация карты с центром в центре масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для рек (если они доступны)
rivers = [
    {'name': 'Shyzhyn River', 'wkt': 'POINT(37.123456 48.987654)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(37.234567 49.098765)'},
    {'name': 'Shilik River', 'wkt': 'POINT(37.345678 49.109876)'},
    {'name': 'Shynzhaly River', 'wkt': 'POINT(37.456789 49.210987)'}
]

# Преобразование WKT в геометрию
rivers_gdf = gpd.GeoDataFrame(rivers, geometry=[wkt.loads(r['wkt']) for r in rivers])
rivers_gdf.crs = 'EPSG:4326'

# Добавление рек на карту
for _, row in rivers_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Поиск притока и расстояние до слияния
def find_confluence_and_distance(river1, river2):
    if river1.intersects(river2):
        return 0, None
    else:
        distance = river1.distance(river2)
        return distance, (river1.centroid.x + river2.centroid.x) / 2, (river1.centroid.y + river2.centroid.y) / 2

# Пример проверки для двух рек
river1 = rivers_gdf[rivers_gdf['name'] == 'Shyzhyn River'].geometry.iloc[0]
river2 = rivers_gdf[rivers_gdf['name'] == 'Byzhy River'].geometry.iloc[0]

distance, confluence_x, confluence_y = find_confluence_and_distance(river1, river2)

if distance is not None:
    folium.Marker([confluence_y, confluence_x], popup=f"Слияние на расстоянии {distance} м").add_to(m)
else:
    folium.Marker([river1.centroid.y, river1.centroid.x], popup="Приток найден").add_to(m)

# Сохранение карты
m.save("104.html")