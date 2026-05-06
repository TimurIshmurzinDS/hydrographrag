import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту как GeoJSON-объект с зеленой заливкой и темно-зеленой границей
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдательных точек
observation_points = [
    {
        'location': wkt.loads('POINT(55.123456 37.654321)'),
        'description': 'Наблюдение на расстоянии 0,2 км выше места слияния с рекой Osek River'
    },
    {
        'location': wkt.loads('POINT(55.234567 38.765432)'),
        'description': 'Наблюдение на расстоянии 0,2 км выше места слияния с рекой Osek River'
    },
    {
        'location': wkt.loads('POINT(55.345678 39.876543)'),
        'description': 'Наблюдение на расстоянии 0,2 км выше места слияния с рекой Osek River'
    }
]

# Добавление наблюдательных точек на карту
for point in observation_points:
    folium.Marker(point['location'], 
                  popup=point['description']).add_to(m)

# Сохранение карты в файл
m.save("68.html")