import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат притоков (если они есть в WKT формате)
primal_rivers_wkt = [
    {'name': 'Koktal River', 'wkt': 'LINESTRING(10 10, 20 20)'},
    {'name': 'Bayankol River', 'wkt': 'LINESTRING(30 30, 40 40)'}
]

# Преобразование WKT в GeoDataFrame
primal_rivers_gdf = gpd.GeoDataFrame(primal_rivers_wkt, geometry=[wkt.loads(r['wkt']) for r in primal_rivers_wkt])

# Фильтрация притоков реки Каратал (пример условий)
primal_rivers_filtered = primal_rivers_gdf[primal_rivers_gdf.geometry.intersects(basin_data.geometry.unary_union)]

# Суммирование протяженности притоков
total_length_km = primal_rivers_filtered['Length_km'].sum()

print(f"Общая протяженность притоков реки Каратал: {total_length_km} км")

# Сохранение карты
m.save("93.html")