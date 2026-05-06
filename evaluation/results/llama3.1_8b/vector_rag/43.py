import geopandas as gpd
import folium
from shapely import wkt

# Загрузка шапфайла с внешними полигонными границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создание списка наблюдаемых точек
obs_points = [
    {'lat': 43.1234, 'lon': 77.4567},
    {'lat': 43.2345, 'lon': 78.5678}
]

# Добавление наблюдаемых точек на карту
for point in obs_points:
    folium.Marker([point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("43.html")