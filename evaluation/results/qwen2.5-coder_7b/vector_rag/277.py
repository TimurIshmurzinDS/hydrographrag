import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о прибыльности акций технологического сектора (замените на реальные данные)
profit_data = [
    {'company': 'TechCorp', 'year': 2019, 'profit': 500},
    {'company': 'TechCorp', 'year': 2020, 'profit': 600},
    {'company': 'TechCorp', 'year': 2021, 'profit': 700},
    {'company': 'Innovate Inc.', 'year': 2019, 'profit': 450},
    {'company': 'Innovate Inc.', 'year': 2020, 'profit': 550},
    {'company': 'Innovate Inc.', 'year': 2021, 'profit': 650}
]

# Пример данных о местоположении компаний (замените на реальные данные)
coordinates_data = [
    {'company': 'TechCorp', 'wkt': 'POINT(37.422 -122.084)'},
    {'company': 'Innovate Inc.', 'wkt': 'POINT(37.425 -122.086)'}
]

# Добавление маркеров компаний на карту
for coord in coordinates_data:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['company']).add_to(m)

# Сохранение карты в файл
m.save("277.html")