import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Karkara River
river_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине реки
m = folium.Map(location=[river_data.centroid.y, river_data.centroid.x], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(data=river_data.to_json(), name='basin').add_to(m)

# Создание списка с данными о расходе воды
water_consumption_data = [
    {'date': '2020-01-01', 'value': 100},
    {'date': '2019-01-01', 'value': 120},
    # Данные за предыдущие десятилетия
    {'date': '2010-01-01', 'value': 80},
    {'date': '2009-01-01', 'value': 90}
]

# Рассчет среднего расхода воды за последние 10 лет и предыдущие 10 лет
last_decade_consumption = sum([data['value'] for data in water_consumption_data[-10:]]) / len(water_consumption_data[-10:])
previous_decade_consumption = sum([data['value'] for data in water_consumption_data[:-10]]) / len(water_consumption_data[:-10])

# Рассчет разницы в расходе воды
consumption_difference = last_decade_consumption - previous_decade_consumption

print(f"Разница в расходе воды за последние 10 лет и предыдущие 10 лет: {consumption_difference}")

# Сохранение карты
m.save("54.html")