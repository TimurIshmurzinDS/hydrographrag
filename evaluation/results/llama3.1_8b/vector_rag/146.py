import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'name': 'Аягоз', 'coords': wkt.loads('POINT(75.123 46.456)')},
    {'name': 'Токыраун', 'coords': wkt.loads('POINT(77.890 45.678)')}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coords'].coords[0], popup=coord['name']).add_to(m)

# Сохранить карту в файл
m.save("146.html")