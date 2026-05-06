import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
                name='Бассейн',
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений в виде словарей
observations = [
    {'lat': 55.123456, 'lon': 36.789012},
    {'lat': 55.124567, 'lon': 36.790123},
    {'lat': 55.125678, 'lon': 36.791234},
    {'lat': 55.126789, 'lon': 36.792345}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker([observation['lat'], observation['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("230.html")