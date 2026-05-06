import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат наблюдений (WKT)
observations = [
    {'wkt': 'POINT(10.5 48.3)', 'level': 1.2},
    {'wkt': 'POINT(10.6 48.4)', 'level': 1.5},
    {'wkt': 'POINT(10.7 48.5)', 'level': 1.3}
]

# Преобразование координат в геометрические объекты
observation_geoms = [wkt.loads(obs['wkt']) for obs in observations]
observation_levels = [obs['level'] for obs in observations]

# Нахождение максимального уровня воды
max_level = max(observation_levels)

# Вывод максимального уровня воды
print(f"Максимальный уровень воды, достигнутый во время последнего весеннего паводка на реке Osek River: {max_level} м")

# Сохранение карты
m.save("19.html")