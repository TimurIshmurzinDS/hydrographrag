import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о реках из файла shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_child(
    folium.features.GeoJsonTooltip(fields=['name'], aliases=['Название области'], labels=True)
).add_to(m)

# Создать список с координатами (WKT) рек
coordinates = [
    {'type': 'Feature', 'geometry': wkt.loads('POLYGON ((30 40, 40 40, 40 50, 30 50, 30 40))'), 'properties': {'name': 'Lepsy River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POLYGON ((35 45, 45 45, 45 55, 35 55, 35 45))'), 'properties': {'name': 'Dos River'}}
]

# Добавить координаты на карту
folium.GeoJson(coordinates).add_to(m)

# Сохранить карту в файл
m.save("128.html")