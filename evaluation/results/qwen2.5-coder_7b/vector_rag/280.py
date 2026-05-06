import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на границе бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о стоимости проживания в крупных городах (hardcoded)
cities_data = [
    {'city': 'Москва', 'year': 1900, 'cost': 50},
    {'city': 'Санкт-Петербург', 'year': 1900, 'cost': 60},
    {'city': 'Новгород', 'year': 1900, 'cost': 40},
    {'city': 'Москва', 'year': 2000, 'cost': 500},
    {'city': 'Санкт-Петербург', 'year': 2000, 'cost': 600},
    {'city': 'Новгород', 'year': 2000, 'cost': 400}
]

# Визуализация данных на карте
for city_data in cities_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Город: {city_data['city']}, Год: {city_data['year']}, Стоимость проживания: {city_data['cost']} руб.",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("280.html")