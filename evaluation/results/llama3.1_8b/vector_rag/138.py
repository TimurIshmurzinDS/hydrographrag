import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123, 'lon': 36.456},
    {'lat': 55.789, 'lon': 37.012}
]

# Добавление точек на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сравнение текущих уровней воды в реках Лепсы и Бутак (предположительно, что данные доступны)
water_levels = {
    'Butak River': 1.2,
    'Lepsa River': 0.8
}

# Добавление информации о водном уровне на карту
for river, level in water_levels.items():
    folium.Marker(location=[55.678, 36.901], popup=f'Водный уровень в реке {river}: {level} м').add_to(m)

# Сохранение карты в файл
m.save("138.html")