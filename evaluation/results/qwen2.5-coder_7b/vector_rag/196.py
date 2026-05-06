import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о расходе воды (замените на реальные данные)
water_consumption_koksu = [
    {'date': '2013-01', 'value': 500},
    {'date': '2013-02', 'value': 600},
    # ... другие значения за последние 10 лет
]

water_consumption_emel = [
    {'date': '2013-01', 'value': 450},
    {'date': '2013-02', 'value': 550},
    # ... другие значения за последние 10 лет
]

# Визуализация данных о расходе воды на карте
for data in water_consumption_koksu:
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Koksu River: {data["value"]} m³'
    ).add_to(m)

for data in water_consumption_emel:
    folium.CircleMarker(
        location=[centroid.y, centroid.x],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        popup=f'Emel River: {data["value"]} m³'
    ).add_to(m)

# Сохранение карты
m.save("196.html")