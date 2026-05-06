import geopandas as gpd
import folium
from shapely import wkt

# Загрузить геоданные о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и добавить бассейн на карту как GeoJson-объект
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt, name='basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если в контексте присутствуют координаты (WKT), создать список словарей для представления этих координат
wkt_coords = [
    {"lat": 55.123456, "lon": 37.654321},
    {"lat": 55.234567, "lon": 38.765432}
]

# Сохранить карту в файл с именем "242.html"
m.save("242.html")