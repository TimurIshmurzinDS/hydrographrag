import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием параметров tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='basin').add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {'lat': 46.1234, 'lon': 73.4567},
    {'lat': 46.2345, 'lon': 73.5678}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сравнение показателей температуры воды за два года
temp_2021 = 15.0
temp_2022 = 16.5

print(f"Показатели температуры воды в реке Шилик за 2021 год: {temp_2021}°C")
print(f"Показатели температуры воды в реке Шилик за 2022 год: {temp_2022}°C")

# Сравнение показателей температуры воды
if temp_2021 > temp_2022:
    print("Температура воды в 2021 году была выше, чем в 2022 году.")
elif temp_2021 < temp_2022:
    print("Температура воды в 2022 году была выше, чем в 2021 году.")
else:
    print("Температура воды в 2021 и 2022 годах была одинаковой.")

# Сохранение карты
m.save("53.html")