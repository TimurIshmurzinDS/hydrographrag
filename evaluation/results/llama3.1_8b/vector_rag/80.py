import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка словарей с координатами (WKT) рек
tokyraun_coords = [
    {'name': 'Tokyraun River', 'coords': wkt.loads('POLYGON ((40.1234 50.5678, 40.2345 50.6789, ...))')},
    {'name': 'Koktal River', 'coords': wkt.loads('POLYGON ((41.3456 51.7890, 41.4567 51.8901, ...))')}
]

# Рассчет показателей расхода на реках
for river in tokyraun_coords:
    if river['name'] == 'Tokyraun River':
        water_consumption = 100  # примерное значение потребления воды в кубических метрах
    elif river['name'] == 'Koktal River':
        water_consumption = 50  # примерное значение потребления воды в кубических метрах

# Добавление информации о показателях расхода на карту
folium.Marker([40.1234, 50.5678], popup=f'Показатель расхода на Tokyraun River: {water_consumption} м³').add_to(m)
folium.Marker([41.3456, 51.7890], popup=f'Показатель расхода на Koktal River: {water_consumption} м³').add_to(m)

# Сохранение карты в файл
m.save("80.html")