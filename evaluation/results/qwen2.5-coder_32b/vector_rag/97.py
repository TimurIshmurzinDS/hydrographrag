import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с центроидом бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что данные о руслах рек содержатся в поле 'geometry' и имеют тип LineString
# Для примера создадим список словарей с координатами (WKT) для каждой из рек
rivers = [
    {'name': 'Karatal River', 'wkt': 'LINESTRING(75.0 42.0, 76.0 43.0, 77.0 44.0)'},
    {'name': 'Emel River', 'wkt': 'LINESTRING(74.0 41.0, 75.0 42.0)'},
    {'name': 'Koktal River', 'wkt': 'LINESTRING(73.0 40.0, 74.0 41.0)'},
    {'name': 'Kumbel River', 'wkt': 'LINESTRING(78.0 45.0, 79.0 46.0)'},
    {'name': 'Bayankol River', 'wkt': 'LINESTRING(72.0 39.0, 73.0 40.0)'}
]

# Преобразование WKT в геометрию и добавление на карту
for river in rivers:
    geom = wkt.loads(river['wkt'])
    folium.PolyLine(locations=geom.coords, color='blue', weight=2.5, opacity=1).add_to(m)
    # Проверка, является ли река Емель притоком реки Каратал
    if river['name'] == 'Emel River':
        emel_geom = geom
    elif river['name'] == 'Karatal River':
        karatal_geom = geom

# Проверка пересечения и вычисление длины участка
if emel_geom.intersects(karatal_geom):
    intersection_point = emel_geom.intersection(karatal_geom)
    emel_branch = emel_geom.intersection(gpd.GeoSeries([intersection_point], crs='EPSG:4326').buffer(0.1))
    branch_length = emel_branch.length.iloc[0]
    print(f"Река Емель является притоком реки Каратал. Длина участка до точки слияния: {branch_length} градусов.")
else:
    print("Река Емель не является притоком реки Каратал.")

# Сохранение карты
m.save("97.html")