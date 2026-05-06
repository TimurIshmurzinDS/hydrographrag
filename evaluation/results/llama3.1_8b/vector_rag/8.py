import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile в геопандас
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений (предполагается, что координаты одинаковы)
observations = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012}
]

# Добавление наблюдений на карту
for obs in observations:
    folium.Marker([obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("8.html")