import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами постов мониторинга
monitoring_points = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543},
    {'lat': 43.3456, 'lon': 76.7654}
]

# Добавление постов мониторинга на карту
for point in monitoring_points:
    folium.Marker([point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("62.html")