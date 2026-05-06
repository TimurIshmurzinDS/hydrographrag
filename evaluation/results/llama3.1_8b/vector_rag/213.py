import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водостоке Dos River из shapefile
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с использованием библиотеки Folium и добавление гидрологических данных на карту
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Преобразование показаний датчиков в прогноз цены на Ethereum (тут мы будем использовать hardcoded список словарей)
coordinates = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 55.7632, 'lon': 37.6234},
    {'lat': 55.7706, 'lon': 37.6295}
]

# Добавление координат на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("213.html")