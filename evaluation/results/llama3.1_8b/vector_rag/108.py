import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты с центроидом бассейна
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление контура бассейна на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат (WKT) для отображения на карте
wkt_coords = [
    {'lat': 52.1234, 'lon': 45.6789},
    {'lat': 51.2345, 'lon': 46.7890}
]

# Добавление координат на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("108.html")