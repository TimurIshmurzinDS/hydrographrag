import geopandas as gpd
import folium
from shapely import wkt

# Загрузка и преобразование данных из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центроидов области
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы области на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о добыче золота (замените на реальные данные)
gold_extraction_data = [
    {'year': 1850, 'volume': 10},
    {'year': 1860, 'volume': 15},
    {'year': 1870, 'volume': 20},
    {'year': 1880, 'volume': 25},
    {'year': 1890, 'volume': 30},
    {'year': 1900, 'volume': 40},
    {'year': 1910, 'volume': 50},
    {'year': 1920, 'volume': 60},
    {'year': 1930, 'volume': 70},
    {'year': 1940, 'volume': 80},
    {'year': 1950, 'volume': 90},
    {'year': 1960, 'volume': 100},
    {'year': 1970, 'volume': 110},
    {'year': 1980, 'volume': 120},
    {'year': 1990, 'volume': 130},
    {'year': 2000, 'volume': 140},
    {'year': 2010, 'volume': 150},
    {'year': 2020, 'volume': 160}
]

# Визуализация данных о добыче золота на карте
for data in gold_extraction_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Год: {data['year']}, Объем добычи: {data['volume']} тонн",
        icon=folium.Icon(color='gold', icon='star')
    ).add_to(m)

# Сохранение карты
m.save("274.html")