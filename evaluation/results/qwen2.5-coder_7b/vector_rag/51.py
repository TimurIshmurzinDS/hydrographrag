import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных расхода воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2021-06-01', 'value': 500},
    {'date': '2021-07-01', 'value': 450},
    {'date': '2021-08-01', 'value': 520},
    {'date': '2021-09-01', 'value': 480},
    {'date': '2021-10-01', 'value': 530},
    {'date': '2021-11-01', 'value': 470},
    {'date': '2021-12-01', 'value': 510},
    {'date': '2022-06-01', 'value': 505},
    {'date': '2022-07-01', 'value': 455},
    {'date': '2022-08-01', 'value': 525},
    {'date': '2022-09-01', 'value': 490},
    {'date': '2022-10-01', 'value': 535},
    {'date': '2022-11-01', 'value': 475},
    {'date': '2022-12-01', 'value': 515}
]

# Расчет среднего расхода воды в летний и зимний периоды
summer_values = [data['value'] for data in water_consumption_data if data['date'].split('-')[1] in ['06', '07', '08', '09', '10']]
winter_values = [data['value'] for data in water_consumption_data if data['date'].split('-')[1] in ['11', '12', '01', '02', '03']]

summer_average = sum(summer_values) / len(summer_values)
winter_average = sum(winter_values) / len(winter_values)

print(f"Средний расход воды в летнем периоде: {summer_average}")
print(f"Средний расход воды в зимнем периоде: {winter_average}")

# Сохранение карты
m.save("51.html")