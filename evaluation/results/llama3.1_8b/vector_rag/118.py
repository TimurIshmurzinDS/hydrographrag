import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о водосборе
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области водосбора и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область водосбора на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создать список словарей с координатами (WKT) рек
river_coords = [
    {'name': 'Temirlik River', 'coords': wkt.loads('POLYGON ((40.1234 50.5678, 40.2345 50.6789, 40.3456 50.7890, 40.4567 50.8901))')},
    {'name': 'Sarykan River', 'coords': wkt.loads('POLYGON ((41.1234 51.5678, 41.2345 51.6789, 41.3456 51.7890, 41.4567 51.8901))')}
]

# Добавить реки на карту
for river in river_coords:
    folium.GeoJson(river['coords'].wkt).add_to(m)

# Сохранить карту в файл
m.save("118.html")