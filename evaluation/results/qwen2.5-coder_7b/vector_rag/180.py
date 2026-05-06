import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о речной сети
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid базина
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат наблюдений (WKT)
observations = [
    {'wkt': 'POINT(65.1234 45.6789)', 'label': 'Наблюдение 1'},
    {'wkt': 'POINT(65.2345 45.7890)', 'label': 'Наблюдение 2'},
    {'wkt': 'POINT(65.3456 45.8901)', 'label': 'Наблюдение 3'},
    {'wkt': 'POINT(65.4567 45.9012)', 'label': 'Наблюдение 4'}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.Marker([point.y, point.x], popup=obs['label']).add_to(m)

# Сохранение карты
m.save("180.html")