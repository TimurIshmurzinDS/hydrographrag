import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область на карте
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_child(
    folium.features.GeoJsonTooltip(fields=['name'], aliases=['Название области'], labels=True)
).add_to(m)

# Создать список словарей с координатами (WKT) рек
coordinates = [
    {'name': 'Река Курты', 'wkt': wkt.loads('POINT(48.123 77.456)')},
    {'name': 'Река Шарын', 'wkt': wkt.loads('POINT(49.789 78.321)')},
    {'name': 'Река Шизжин', 'wkt': wkt.loads('POINT(47.654 76.987)')},
    {'name': 'Река Сарыкан', 'wkt': wkt.loads('POINT(50.123 79.456)')},
    {'name': 'Река Узен-Каргалы', 'wkt': wkt.loads('POINT(48.789 77.321)')}
]

# Добавить точки на карту
for coord in coordinates:
    folium.Marker(location=coord['wkt'].coords[0], popup=coord['name']).add_to(m)

# Сохранить карту в файл
m.save("123.html")