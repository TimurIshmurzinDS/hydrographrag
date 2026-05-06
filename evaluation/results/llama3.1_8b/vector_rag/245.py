import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами наблюдений
observations = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.1245, 'lon': 76.5443},
    {'lat': 43.1256, 'lon': 76.5454},
    {'lat': 43.1267, 'lon': 76.5465},
    {'lat': 43.1278, 'lon': 76.5476}
]

# Добавить точки наблюдений на карту
for obs in observations:
    folium.Marker(location=[obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("245.html")