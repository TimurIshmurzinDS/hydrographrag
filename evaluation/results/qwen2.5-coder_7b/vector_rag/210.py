import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных для Lepsy River и Aksu River (замените на реальные данные)
data_lepsy = [
    {'date': '2021-01-01', 'flow': 10},
    {'date': '2021-02-01', 'flow': 15},
    {'date': '2021-03-01', 'flow': 20},
    {'date': '2021-04-01', 'flow': 25},
    {'date': '2021-05-01', 'flow': 30},
    {'date': '2021-06-01', 'flow': 35},
    {'date': '2021-07-01', 'flow': 40},
    {'date': '2021-08-01', 'flow': 35},
    {'date': '2021-09-01', 'flow': 30},
    {'date': '2021-10-01', 'flow': 25},
    {'date': '2021-11-01', 'flow': 20},
    {'date': '2021-12-01', 'flow': 15}
]

data_aksu = [
    {'date': '2021-01-01', 'flow': 8},
    {'date': '2021-02-01', 'flow': 13},
    {'date': '2021-03-01', 'flow': 18},
    {'date': '2021-04-01', 'flow': 23},
    {'date': '2021-05-01', 'flow': 28},
    {'date': '2021-06-01', 'flow': 33},
    {'date': '2021-07-01', 'flow': 38},
    {'date': '2021-08-01', 'flow': 33},
    {'date': '2021-09-01', 'flow': 28},
    {'date': '2021-10-01', 'flow': 23},
    {'date': '2021-11-01', 'flow': 18},
    {'date': '2021-12-01', 'flow': 13}
]

# Визуализация данных
for data in [data_lepsy, data_aksu]:
    for point in data:
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=f"Flow: {point['flow']}, Date: {point['date']}",
            icon=folium.Icon(color='red' if data == data_lepsy else 'blue')
        ).add_to(m)

# Сохранение карты
m.save("210.html")