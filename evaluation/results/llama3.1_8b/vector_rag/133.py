import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейнах из shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с границами бассейна
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin').add_to(m)
m

# Если в контексте есть координаты (WKT), создать список словарей с данными о реках и их свойствами
if 'Coordinates' in locals():
    rivers_data = [
        {'name': 'Kurty River', 'type': 'HY_HydroFeature', 'properties': {'Date_water_level_Value': 'исторические данные', 'Basin_are_km²': 'площадь бассейна в квадратных километрах'}},
        {'name': 'Dos River', 'type': 'HY_HydroFeature', 'properties': {'Date_water_level_Value': 'недавние осадки', 'Basin_are_km²': 'площадь бассейна в квадратных километрах'}}
    ]

# Рассчитать влияние недавших осадков на сток реки Dos River относительно исторических данных реки Kurty River
for river in rivers_data:
    if river['name'] == 'Dos River':
        # Рассчитать влияние недавших осадков на сток реки Dos River
        dos_influence = 0.5 * float(river['properties']['Basin_are_km²'])
    elif river['name'] == 'Kurty River':
        # Рассчитать влияние исторических данных на сток реки Kurty River
        kurty_influence = 0.3 * float(river['properties']['Basin_are_km²'])

# Сохранить карту в файл
m.save("133.html")