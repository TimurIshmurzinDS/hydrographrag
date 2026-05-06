import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf.crs = 'EPSG:4326'

# 2. Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# 3. Добавить бассейн на карту
folium.GeoJson(gdf.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Batareyka River Basin',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создать список словарей с координатами (WKT)
wkt_coords = [
    {"lat": 55.123456, "lon": 37.654321},
    {"lat": 55.234567, "lon": 38.765432}
]

# 5. Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Пункт наблюдения').add_to(m)

# 6. Сохранить карту в файл
m.save("212.html")